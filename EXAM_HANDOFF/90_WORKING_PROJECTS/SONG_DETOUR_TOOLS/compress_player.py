from pathlib import Path
import json
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent / 'WLAD_ELHALAL_SPEAKER'
sys.path.insert(0, str(HERE / 'python'))
import imageio_ffmpeg
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
wav = PROJECT/'Audio/clip_ima.wav'
subprocess.run([ffmpeg,'-v','error','-y','-ss','45','-i',str(HERE/'source.webm'),
    '-t','6','-vn','-ac','1','-ar','8000','-af',
    'volume=0.5,afade=t=in:d=0.02,afade=t=out:st=5.98:d=0.02',
    '-c:a','adpcm_ima_wav','-block_size','256',str(wav)],check=True)
raw = wav.read_bytes()
chunks = {}
pos = 12
while pos+8 <= len(raw):
    tag,size = struct.unpack_from('<4sI',raw,pos)
    chunks[tag] = raw[pos+8:pos+8+size]
    pos += 8+size+(size&1)
fmt = struct.unpack_from('<HHIIHH',chunks[b'fmt '])
assert fmt[0]==17 and fmt[1]==1 and fmt[2]==8000 and fmt[4]==256 and fmt[5]==4
payload = chunks[b'data']
samples_per_block = struct.unpack_from('<H',chunks[b'fmt '],18)[0]
assert samples_per_block == 505
assert len(payload)//256 * 505 >= 48000

steps = [7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767]
changes = [-1,-1,-1,-1,2,4,6,8]
decoded = []
for b in range(0,len(payload),256):
    block = payload[b:b+256]
    value,index,_ = struct.unpack_from('<hBB',block)
    assert 0 <= index <= 88
    decoded.append(value)
    for byte in block[4:]:
        for code in (byte&15,byte>>4):
            delta = ((2*(code&7)+1)*steps[index])>>3
            value = max(-32768,min(32767,value + (-delta if code&8 else delta)))
            index = max(0,min(88,index+changes[code&7]))
            decoded.append(value)
reference = subprocess.run([ffmpeg,'-v','error','-i',str(wav),'-f','s16le','-'],capture_output=True,check=True).stdout
assert list(struct.unpack('<%dh'%(len(reference)//2),reference))[:48000] == decoded[:48000], 'Decoder mismatch'
subprocess.run([ffmpeg,'-v','error','-y','-i',str(wav),'-t','6',str(PROJECT/'Audio/preview.wav')],check=True)
header = '#ifndef SONG_SAMPLES_H\n#define SONG_SAMPLES_H\n#include <stdint.h>\n'
header += '#define SONG_SAMPLE_RATE 8000u\n#define SONG_SAMPLE_COUNT 48000u\n'
header += '#define SONG_BLOCK_SIZE 256u\n#define SONG_BLOCK_SAMPLES 505u\n'
header += 'static const uint8_t song_samples[%d] = {\n'%len(payload)
header += '\n'.join('    '+','.join(map(str,payload[i:i+32]))+',' for i in range(0,len(payload),32))
header += '\n};\n#endif\n'
(PROJECT/'Source/song_samples.h').write_text(header,encoding='ascii')
decoder = '''#ifndef SONG_DECODER_H
#define SONG_DECODER_H
#include "song_samples.h"

/* IMA ADPCM: a block starts with a full signed sample and a step index.
   Following bytes contain two compressed samples, low nibble first. */
static int32_t song_next_sample(void)
{
    static uint32_t block = 0;
    static uint32_t within = 0;
    static int32_t value = 0;
    static int32_t index = 0;
    static const int8_t changes[8] = {-1,-1,-1,-1,2,4,6,8};
    static const int16_t steps[89] = {STEPS};
    uint32_t code;
    uint32_t packed;
    int32_t delta;

    if (within == 0)
    {
        value = song_samples[block] | ((uint32_t)song_samples[block + 1] << 8);
        if (value >= 32768) value -= 65536;
        index = song_samples[block + 2];
    }
    else
    {
        packed = song_samples[block + 4 + (within - 1) / 2];
        code = ((within - 1) & 1) ? (packed >> 4) : (packed & 15);
        delta = ((2 * (int32_t)(code & 7) + 1) * steps[index]) >> 3;
        value += (code & 8) ? -delta : delta;
        if (value > 32767) value = 32767;
        if (value < -32768) value = -32768;
        index += changes[code & 7];
        if (index < 0) index = 0;
        if (index > 88) index = 88;
    }
    within++;
    if (within == SONG_BLOCK_SAMPLES)
    {
        within = 0;
        block += SONG_BLOCK_SIZE;
    }
    return value;
}
#endif
'''.replace('STEPS',','.join(map(str,steps)))
(PROJECT/'Source/song_decoder.h').write_text(decoder,encoding='ascii')
main = PROJECT/'Source/sample.c'
main.write_text(main.read_text().replace('EXAM_TIMER0, 16000','EXAM_TIMER0, 8000'),encoding='ascii')
irq = PROJECT/'Source/timer/IRQ_timer.c'
irq.write_text(irq.read_text().replace('#include "song_samples.h"','#include "song_decoder.h"').replace(
    'exam_dac_write((int32_t)song_samples[position] << 2);',
    'exam_dac_write((song_next_sample() + 32768) >> 6);'),encoding='ascii')
meta_path = PROJECT/'Audio/source.json'
meta = json.loads(meta_path.read_text(encoding='utf-8'))
meta.update(duration_seconds=6,sample_rate=8000,encoding='IMA ADPCM mono, 256-byte blocks',
    sample_count=48000,compressed_bytes=len(payload),
    processing='Half gain, 20 ms fades; decoded signed 16-bit PCM mapped to 10-bit DAC.',
    decoder_validation='All 48000 output samples match FFmpeg decoding exactly.')
meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old_pcm = PROJECT/'Audio/clip_u8.pcm'
assert old_pcm.resolve().parent == (PROJECT/'Audio').resolve()
old_pcm.unlink(missing_ok=True)
print('PASS: 48000 decoder samples match FFmpeg. Compressed bytes:',len(payload))

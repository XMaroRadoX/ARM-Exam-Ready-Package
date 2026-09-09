from pathlib import Path
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE / 'python'))
import imageio_ffmpeg

template = ROOT / '01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API'
project = ROOT / '90_WORKING_PROJECTS/WLAD_ELHALAL_SPEAKER'
if project.exists():
    raise SystemExit('Destination exists; refusing to overwrite it.')
project.mkdir()
for folder in ('Source', 'RTE', 'DebugConfig'):
    if (template / folder).exists():
        shutil.copytree(template / folder, project / folder)
for name in ('sample.uvprojx', 'sample.uvoptx', 'sample.sct'):
    shutil.copy2(template / name, project / name)
for name in ('Objects', 'Listings', 'Audio'):
    (project / name).mkdir()

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
pcm = project / 'Audio/clip_u8.pcm'
subprocess.run([ffmpeg, '-v', 'error', '-y', '-ss', '45', '-i', str(HERE / 'source.webm'),
    '-t', '20', '-vn', '-ac', '1', '-ar', '16000', '-af',
    'volume=0.5,afade=t=in:d=0.02,afade=t=out:st=19.98:d=0.02',
    '-c:a', 'pcm_u8', '-f', 'u8', str(pcm)], check=True)
data = pcm.read_bytes()
assert len(data) == 320000, len(data)
subprocess.run([ffmpeg, '-v', 'error', '-y', '-f', 'u8', '-ar', '16000', '-ac', '1',
    '-i', str(pcm), str(project / 'Audio/preview.wav')], check=True)
header = '#ifndef SONG_SAMPLES_H\n#define SONG_SAMPLES_H\n#include <stdint.h>\n'
header += '#define SONG_SAMPLE_RATE 16000u\n#define SONG_SAMPLE_COUNT 320000u\n'
header += 'static const uint8_t song_samples[SONG_SAMPLE_COUNT] = {\n'
header += '\n'.join('    ' + ','.join(map(str, data[i:i+32])) + ',' for i in range(0, len(data), 32))
header += '\n};\n#endif\n'
(project / 'Source/song_samples.h').write_text(header, encoding='ascii')
(project / 'Source/sample.c').write_text('''#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
    exam_init();
    exam_led_clear();
    exam_dac_init();
    exam_dac_write(512);

    if (exam_timer_config_hz(EXAM_TIMER0, 16000, EXAM_TIMER_PERIODIC) != EXAM_OK)
    {
        exam_led_on(6);
        while (1) { __WFI(); }
    }

    exam_led_on(4);
    exam_timer_start(EXAM_TIMER0);
    while (1) { __WFI(); }
}
''', encoding='ascii')
irq = project / 'Source/timer/IRQ_timer.c'
source = irq.read_text()
start = source.index('void TIMER0_IRQHandler')
end = source.index('void TIMER1_IRQHandler', start)
source = source[:start] + '''/* One audio sample per interrupt; reset the board to replay. */
void TIMER0_IRQHandler(void)
{
    static uint32_t position = 0;
    uint32_t pending = exam_timer_ack(EXAM_TIMER0);

    if (exam_timer_match_happened(pending, 0))
    {
        if (position < SONG_SAMPLE_COUNT)
        {
            exam_dac_write((int32_t)song_samples[position] << 2);
            position++;
        }
        else
        {
            exam_timer_stop(EXAM_TIMER0);
            exam_dac_write(512);
            exam_led_off(4);
            exam_led_on(5);
        }
    }
}

''' + source[end:]
source = source.replace('#include "exam_api.h"', '#include "exam_api.h"\n#include "song_samples.h"')
irq.write_text(source, encoding='ascii')
metadata = json.loads((HERE / 'source.info.json').read_text(encoding='utf-8'))
(project / 'Audio/source.json').write_text(json.dumps(dict(
    title=metadata['title'], url='https://www.youtube.com/watch?v=tcZgr2oM6kg',
    start_seconds=45, duration_seconds=20, sample_rate=16000,
    encoding='unsigned 8-bit mono PCM', sample_count=len(data),
    processing='Half gain, 20 ms fade in/out; DAC samples shifted left by 2.'
), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared separate player; 320000 samples, 20 seconds at 16 kHz.')

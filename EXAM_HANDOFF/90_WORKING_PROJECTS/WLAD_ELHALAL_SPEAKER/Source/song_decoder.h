#ifndef SONG_DECODER_H
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
    static const int16_t steps[89] = {7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767};
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

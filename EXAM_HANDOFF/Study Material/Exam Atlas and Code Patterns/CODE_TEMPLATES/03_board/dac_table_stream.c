/* Recommended exam template: stream a table through DAC from a timer. */
#include "exam_api.h"

static const uint16_t samples[] = {0u, 256u, 512u, 768u, 1023u, 768u, 512u, 256u};
static volatile uint32_t sample_index;

static void dac_timer_callback(uint8_t timer, uint32_t flags) {
    if (timer != 0u || !exam_timer_match_happened(flags, 0u)) return;
    (void)exam_dac_write(samples[sample_index]);
    sample_index++;
    if (sample_index == (sizeof(samples) / sizeof(samples[0]))) sample_index = 0u;
}

exam_status_t dac_stream_init(void) {
    sample_index = 0u;
    return exam_timer_every_hz(0, 8000, dac_timer_callback);
}

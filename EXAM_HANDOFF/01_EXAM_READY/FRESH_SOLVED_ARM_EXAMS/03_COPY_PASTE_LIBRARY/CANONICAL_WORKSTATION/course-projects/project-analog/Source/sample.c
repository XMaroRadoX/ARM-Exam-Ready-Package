#include "exam_api.h"
static void stop_on_error(void) { exam_led_write(0xFFu); for (;;) {} }

int main(void)
{
    uint8_t in_flight=0u;
    exam_init();
    exam_adc_init();
    exam_dac_init();
    if (exam_timer_config_ms(EXAM_TIMER0,50u,EXAM_TIMER_PERIODIC)!=EXAM_OK)
        stop_on_error();
    exam_timer_start(EXAM_TIMER0);
    for (;;) {
        uint16_t sample;
        if (exam_adc_take(&sample)) {
            in_flight=0u;
            uint32_t scaled=((uint32_t)sample*1023u)/4095u;
            if (exam_dac_write((int32_t)scaled)!=EXAM_OK) stop_on_error();
            exam_adc_show_high8(sample);
        }
        if ((exam_events_take(1u)&1u) && !in_flight) {
            in_flight=1u;
            exam_adc_start();
        }
    }
}

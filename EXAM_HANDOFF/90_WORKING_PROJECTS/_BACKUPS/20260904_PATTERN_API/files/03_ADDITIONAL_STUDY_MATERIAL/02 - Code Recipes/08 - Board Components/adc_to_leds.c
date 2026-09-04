/* Recommended exam template: potentiometer's top eight ADC bits on LEDs. */
#include "exam_api.h"

exam_status_t adc_led_init(void) {
    exam_adc_init();
    exam_adc_start();
    return EXAM_OK;
}

void adc_led_loop(void) {
    uint16_t sample;
    if (exam_adc_take(&sample) != 0u) {
        /* ADC is 12 bit; bits 11..4 become the displayed byte. */
        exam_led_write((uint8_t)(((uint32_t)sample >> 4) & 0xFFu));
        exam_adc_start();
    }
}

/* Recommended exam template: potentiometer's top eight ADC bits on LEDs. */
#include "exam_api.h"

exam_status_t adc_led_init(void) {
    return exam_pot_start();
}

void adc_led_loop(void) {
    int sample;
    if (exam_pot_read(&sample) == EXAM_OK) {
        /* ADC is 12 bit; bits 11..4 become the displayed byte. */
        (void)exam_led_write((uint8_t)(((uint32_t)sample >> 4) & 0xFFu));
    }
}

#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
    exam_init();
    exam_led_clear();
    exam_dac_init();
    exam_dac_write(512);

    if (exam_timer_config_hz(EXAM_TIMER0, 8000, EXAM_TIMER_PERIODIC) != EXAM_OK)
    {
        exam_led_on(6);
        while (1) { __WFI(); }
    }

    exam_led_on(4);
    exam_timer_start(EXAM_TIMER0);
    while (1) { __WFI(); }
}

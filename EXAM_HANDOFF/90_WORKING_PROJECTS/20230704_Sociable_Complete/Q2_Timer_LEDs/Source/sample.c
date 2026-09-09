#include "LPC17xx.h"
#include "exam_api.h"

/* Timer 1's handler and the array are in Source/timer/IRQ_timer.c. */
int main(void)
{
    exam_init();
    exam_led_clear();
    if (exam_timer_config_ms(EXAM_TIMER1, 2000u,
                             EXAM_TIMER_PERIODIC) != EXAM_OK) {
        while (1) { __WFI(); }
    }
    exam_timer_start(EXAM_TIMER1);
    while (1) {
        __WFI();
    }
}

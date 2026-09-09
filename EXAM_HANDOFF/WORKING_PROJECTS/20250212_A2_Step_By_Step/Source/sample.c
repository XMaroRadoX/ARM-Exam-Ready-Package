#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
    exam_init();
    exam_dac_init();

    /* Configure Timer 0, but leave it stopped until INT0 is pressed. */
    (void)exam_timer_config_ticks(EXAM_TIMER0, 1263u,
                                  EXAM_TIMER_PERIODIC);

    /* Template core clock: 100 MHz. Timer clock: 100/4 = 25 MHz. */
    (void)exam_timer_set_clock_divider(EXAM_TIMER0, 4u);

    /* Enable buttons after the DAC and timer are ready. */
    exam_buttons_init();

    while (1)
    {
        __WFI();
    }
}

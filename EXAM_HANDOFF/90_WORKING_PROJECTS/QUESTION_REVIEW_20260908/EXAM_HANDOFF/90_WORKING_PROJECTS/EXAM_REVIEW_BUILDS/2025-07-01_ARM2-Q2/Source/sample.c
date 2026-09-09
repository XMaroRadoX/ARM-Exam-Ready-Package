/* Q2: one generated value and one LED every 2.5 seconds.
 * Copy this complete file to Source/sample.c in a WORKING template.
 * Use the supplied IRQ_timer.c replacement: Timer0 is owned here.
 */
#include "LPC17xx.h"
#include "exam_api.h"

/* Compiler passes the first four arguments in R0-R3 and m on the stack. */
extern uint32_t LCGsequence(uint32_t previous, uint32_t a,
                               uint32_t c, uint32_t n, uint32_t m);

void TIMER1_IRQHandler(void)
{
    /* Static locals retain their values between timer interrupts. */
    static uint32_t previous = 6u;
    static uint32_t n = 0u;
    uint32_t pending;
    uint32_t value;
    uint32_t remainder;
    uint8_t led;

    pending = exam_timer_ack(EXAM_TIMER1); /* Read AND clear event flags. */
    if ((pending & 1u) == 0u) {
        return;                           /* Not our MR0 interval event. */
    }
    if (n >= 10u) {
        return;                           /* Never call LCG an 11th time. */
    }

    value = LCGsequence(previous, 157u, 3u, 3u, 256u);
    remainder = value % 4u;
    led = (uint8_t)(4u + remainder);      /* 0->4, 1->5, 2->6, 3->7. */

    exam_led_clear();                     /* Old LED off before new LED on. */
    exam_led_on(led);                      /* Physical board label, not index. */
    previous = value;
    n++;

    if (n == 10u) {
        exam_timer_stop(EXAM_TIMER1);      /* Q2 leaves the last LED lit. */
    }
}

int main(void)
{
    exam_init();
    exam_led_clear();
    if (exam_timer_config_ms(EXAM_TIMER1, 2500u,
                             EXAM_TIMER_PERIODIC) != EXAM_OK) {
        while (1) { }                     /* Configuration failed. */
    }
    exam_timer_start(EXAM_TIMER1);
    while (1) {
        __WFI();                          /* Hardware schedules the work. */
    }
}

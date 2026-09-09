/* Complete replacement for Source/timer/IRQ_timer.c.
 * TIMER1_IRQHandler is defined in the supplied sample.c answer.
 * Keep the unused timer handlers here; do not duplicate Timer0.
 */
#include "LPC17xx.h"
#include "exam_api.h"

void TIMER0_IRQHandler(void) { exam_timer_ack(EXAM_TIMER0); }
void TIMER2_IRQHandler(void) { exam_timer_ack(EXAM_TIMER2); }
void TIMER3_IRQHandler(void) { exam_timer_ack(EXAM_TIMER3); }

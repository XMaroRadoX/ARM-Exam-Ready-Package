#include "exam_api.h"

void TIMER0_IRQHandler(void) {
    uint32_t flags=exam_timer_ack(EXAM_TIMER0);
    if (flags & 1u) exam_events_set(1u);
}
void TIMER1_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER1); }
void TIMER2_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER2); }
void TIMER3_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER3); }

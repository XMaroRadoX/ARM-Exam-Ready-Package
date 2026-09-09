#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
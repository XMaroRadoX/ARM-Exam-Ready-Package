#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t tick_count;
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags, 0u)) {
    ++tick_count;
    exam_led_write((uint8_t)tick_count);
  }
}
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1263u, EXAM_TIMER_PERIODIC));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}

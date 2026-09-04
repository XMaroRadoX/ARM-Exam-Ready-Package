/* Complete project and replacement instructions: ../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects/timer-periodic/README.md
 * Open ../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects/timer-periodic/sample.uvprojx; use its matching assembly file. */
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
  require(exam_timer_config_ms(EXAM_TIMER0, 500u, EXAM_TIMER_PERIODIC));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}

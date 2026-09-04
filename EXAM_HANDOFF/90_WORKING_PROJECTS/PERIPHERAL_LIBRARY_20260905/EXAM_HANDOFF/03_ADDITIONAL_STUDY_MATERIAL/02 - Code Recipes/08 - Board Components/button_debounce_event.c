/* Complete project and replacement instructions: ../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects/buttons-rit-timer/README.md
 * Open ../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects/buttons-rit-timer/sample.uvprojx; use its matching assembly file. */
#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint8_t count;
void EINT0_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_INT0); }
void EINT1_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_KEY2); }
void sample_inputs(void) {
  uint32_t events;
  exam_debounce_tick();
  events = exam_button_events_take();
  if (events & EXAM_BUTTON_EVENT_INT0) ++count;
  if (events & EXAM_BUTTON_EVENT_KEY1) exam_timer_stop(EXAM_TIMER0);
  if (events & EXAM_BUTTON_EVENT_KEY2) {
    exam_timer_reset(EXAM_TIMER0);
    (void)exam_timer_ack(EXAM_TIMER0);
    exam_timer_start(EXAM_TIMER0);
  }
}
void RIT_IRQHandler(void) { exam_rit_ack(); sample_inputs(); }
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags, 0u)) exam_led_write(count);
}
int main(void) {
  exam_init(); exam_buttons_init();
  require(exam_debounce_config(10u,50u));
  require(exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC));
  require(exam_rit_config_ms(10u));
  exam_timer_start(EXAM_TIMER0); exam_rit_start();
  for (;;) {}
}

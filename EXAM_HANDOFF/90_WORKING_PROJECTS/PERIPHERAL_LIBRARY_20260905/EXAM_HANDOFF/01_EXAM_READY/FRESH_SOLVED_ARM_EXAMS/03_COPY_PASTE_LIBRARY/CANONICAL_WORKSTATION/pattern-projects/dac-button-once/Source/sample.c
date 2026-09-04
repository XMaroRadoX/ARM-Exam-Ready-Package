#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
static const uint16_t waveform[8]={512u,768u,1023u,768u,512u,256u,0u,256u};
volatile uint32_t sample_index, completed;
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags,0u)) {
    (void)exam_dac_write(waveform[sample_index]);
    if (++sample_index == 8u) { sample_index=0u; ++completed; exam_timer_stop(EXAM_TIMER0); }
  }
}
void begin_wave(void) {
  sample_index=0u;completed=0u;
  exam_timer_reset(EXAM_TIMER0);(void)exam_timer_ack(EXAM_TIMER0);exam_timer_start(EXAM_TIMER0);
}
void EINT0_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_INT0);if (!exam_timer_is_running(EXAM_TIMER0)) begin_wave(); }
int main(void) {
  exam_init();exam_dac_init();exam_buttons_init();
  require(exam_timer_config_ticks(EXAM_TIMER0,1263u,EXAM_TIMER_PERIODIC));
  /* Wait for an INT0 trigger; busy triggers are ignored. */
  for (;;) {}
}

void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1); }

void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2); }

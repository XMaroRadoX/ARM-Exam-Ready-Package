#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint16_t preview, captured;
volatile uint8_t preview_valid, sequence_active, sequence_index;
volatile uint32_t processed;
void ADC_IRQHandler(void) {
  uint16_t sample;
  exam_adc_irq_capture();
  if (exam_adc_take(&sample)) {
    preview=sample; preview_valid=1u;
    if (!sequence_active) exam_adc_show_high8(sample);
  }
  exam_adc_start();
}
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  if (!preview_valid || sequence_active) return;
  captured=preview; /* Most recent completed conversion at raw IRQ entry. */
  processed=(uint32_t)(captured >> 4); /* Exam high-eight-bit extraction. */
  sequence_index=0u;sequence_active=1u;
  exam_led_write((uint8_t)processed);
  exam_timer_reset(EXAM_TIMER0);(void)exam_timer_ack(EXAM_TIMER0);exam_timer_start(EXAM_TIMER0);
}
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags,0u) && sequence_active) {
    if (++sequence_index == 4u) {
      sequence_active=0u;exam_timer_stop(EXAM_TIMER0);exam_led_clear();
    } else exam_led_write((uint8_t)(processed+sequence_index));
  }
}
int main(void) {
  exam_init();exam_buttons_init();exam_adc_init();
  require(exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC));
  NVIC_SetPriority(ADC_IRQn,2u);NVIC_SetPriority(EINT0_IRQn,2u);NVIC_SetPriority(TIMER0_IRQn,2u);
  exam_adc_start();
  for (;;) {}
}

void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1); }

void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2); }

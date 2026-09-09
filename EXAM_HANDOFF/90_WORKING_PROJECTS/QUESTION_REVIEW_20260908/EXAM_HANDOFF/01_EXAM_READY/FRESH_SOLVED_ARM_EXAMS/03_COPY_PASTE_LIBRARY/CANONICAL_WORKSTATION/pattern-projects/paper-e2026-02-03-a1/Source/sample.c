/* Exam of 3 February 2026: debounced button and stable result display. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

extern uint32_t Look_and_Say(uint32_t digits);

/* Foreground-owned state: IRQs only capture input or publish events. */
static uint8_t latest_value;
static uint8_t have_sample;

void EINT0_IRQHandler(void)
{
  (void)exam_debounce_begin(EXAM_BUTTON_INT0);
}

void RIT_IRQHandler(void)
{
  exam_rit_ack();
  exam_debounce_tick();
}

void ADC_IRQHandler(void) { exam_adc_irq_capture(); }

int main(void)
{
  exam_init();
  exam_buttons_init();
  /* Package debounce recommendation; the paper does not prescribe 10/50 ms. */
  if (exam_debounce_config(10u, 50u) != EXAM_OK ||
      exam_rit_config_ms(10u) != EXAM_OK) {
    exam_led_write(0xFFu);
    for (;;) { __WFI(); }
  }
  exam_rit_start();
  exam_adc_init();
  exam_adc_start();

  for (;;) {
    uint16_t sample;
    if (exam_adc_take(&sample)) {
      uint8_t value = (uint8_t)(sample >> 4);
      /* Hold a computed result until the potentiometer high8 value changes.
         The paper specifies no fixed result-hold duration. */
      if (!have_sample || value != latest_value) exam_led_write(value);
      latest_value = value;
      have_sample = 1u;
      exam_adc_start();
    }
    if ((exam_button_events_take() & EXAM_BUTTON_EVENT_INT0) != 0u && have_sample) {
      exam_led_write((uint8_t)Look_and_Say(latest_value));
    }
    __WFI();
  }
}

/* Exam of 3 February 2026: debounced KEY2 and two-second playback. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

#define EVENT_SEQUENCE_STEP (1u << 0)
extern void Recaman(uint32_t *area, uint8_t length);

/* All sequence/display state belongs to the foreground. */
static uint32_t sequence[255];
static uint8_t latest_value;
static uint8_t have_sample;
static uint8_t sequence_length;
static uint8_t sequence_active;
static uint32_t display_index;

void EINT2_IRQHandler(void)
{
  (void)exam_debounce_begin(EXAM_BUTTON_KEY2);
}

void RIT_IRQHandler(void)
{
  exam_rit_ack();
  exam_debounce_tick();
}

void ADC_IRQHandler(void) { exam_adc_irq_capture(); }

void TIMER0_IRQHandler(void)
{
  if ((exam_timer_ack(EXAM_TIMER0) & 1u) != 0u)
    exam_events_set(EVENT_SEQUENCE_STEP);
}

static void begin_sequence(void)
{
  exam_timer_stop(EXAM_TIMER0);
  exam_timer_reset(EXAM_TIMER0);
  (void)exam_events_take(EVENT_SEQUENCE_STEP);
  sequence_active = 0u;
  sequence_length = latest_value;
  display_index = 0u;
  if (sequence_length == 0u) {
    exam_led_clear();
    return;
  }
  Recaman(sequence, sequence_length);
  exam_led_write((uint8_t)sequence[0]);
  display_index = 1u;
  if (sequence_length > 1u &&
      exam_timer_config_ms(EXAM_TIMER0, 2000u, EXAM_TIMER_PERIODIC) == EXAM_OK) {
    sequence_active = 1u;
    exam_timer_start(EXAM_TIMER0);
  }
}

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
      /* Playback owns the display. After it ends, hold its last value
         until a subsequent potentiometer high8 change restores preview. */
      if (!sequence_active && (!have_sample || value != latest_value))
        exam_led_write(value);
      latest_value = value;
      have_sample = 1u;
      exam_adc_start();
    }
    if ((exam_button_events_take() & EXAM_BUTTON_EVENT_KEY2) != 0u && have_sample)
      begin_sequence();
    if ((exam_events_take(EVENT_SEQUENCE_STEP) & EVENT_SEQUENCE_STEP) != 0u &&
        sequence_active) {
      exam_led_write((uint8_t)sequence[display_index++]);
      if (display_index >= sequence_length) {
        sequence_active = 0u;
        exam_timer_stop(EXAM_TIMER0);
        exam_timer_reset(EXAM_TIMER0);
      }
    }
    __WFI();
  }
}

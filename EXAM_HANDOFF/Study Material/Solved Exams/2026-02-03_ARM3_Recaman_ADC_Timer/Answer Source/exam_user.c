/* Exam of 3 February 2026, ARM3, questions 1 and 2. */
#include "exam_user.h"

extern void Recaman(uint32_t *area, uint8_t length);

static uint32_t sequence[255];
static volatile uint8_t latest_value;
static volatile uint8_t sequence_length;
static volatile uint32_t display_index;

void exam_user_init(void)
{
  (void)exam_pot_start();
  exam_buttons_start(exam_button_event);
  (void)exam_timer_clock_divider(0u, 4u);
  (void)exam_timer_prescaler(0u, 24999u);
}

void exam_user_loop(void)
{
  int sample;

  if (exam_pot_read(&sample) == EXAM_OK) {
    latest_value = (uint8_t)((uint32_t)sample >> 4);
    (void)exam_led_write(latest_value);
  }
}

void exam_button_event(exam_button_t button, exam_button_event_t event)
{
  if ((button != EXAM_BUTTON_KEY2) || (event != EXAM_PRESS)) {
    return;
  }

  sequence_length = latest_value;
  display_index = 0u;
  (void)exam_timer_stop(0u);
  (void)exam_timer_reset(0u);

  if (sequence_length == 0u) {
    exam_leds_off();
    return;
  }

  Recaman(sequence, sequence_length);
  (void)exam_led_write((uint8_t)sequence[0]);
  display_index = 1u;

  if (sequence_length > 1u) {
    (void)exam_timer_match(0u, 0u, 2000u,
                           EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);
    (void)exam_timer_start(0u);
  }
}

void TIMER0_IRQHandler(void)
{
  uint32_t pending = LPC_TIM0->IR & 0x3Fu;

  LPC_TIM0->IR = pending;
  if ((pending & 1u) == 0u) {
    return;
  }

  if (display_index < sequence_length) {
    (void)exam_led_write((uint8_t)sequence[display_index]);
    display_index++;
  }

  if (display_index >= sequence_length) {
    (void)exam_timer_stop(0u);
    (void)exam_timer_reset(0u);
  }
}

void exam_user_10ms_hook(void)
{
}

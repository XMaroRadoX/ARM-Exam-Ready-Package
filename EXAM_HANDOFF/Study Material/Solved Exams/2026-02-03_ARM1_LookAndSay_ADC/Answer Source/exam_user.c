/* Exam of 3 February 2026, ARM1, questions 1 and 2. */
#include "exam_user.h"

extern uint32_t Look_and_Say(uint32_t digits);

static volatile uint8_t latest_value;

void exam_user_init(void)
{
  (void)exam_pot_start();
  exam_buttons_start(exam_button_event);
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
  uint32_t result;

  if ((button == EXAM_BUTTON_INT0) && (event == EXAM_PRESS)) {
    result = Look_and_Say(latest_value);
    (void)exam_led_write((uint8_t)result);
  }
}

void exam_user_10ms_hook(void)
{
}

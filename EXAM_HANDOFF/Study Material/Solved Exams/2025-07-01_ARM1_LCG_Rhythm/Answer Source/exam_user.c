/* Exam of 1 July 2025, ARM1, questions 1 to 3. */
#include "exam_user.h"

extern uint32_t nextElementLCG(uint32_t previous,
                               uint32_t multiplier,
                               uint32_t increment,
                               uint32_t index,
                               uint32_t modulus);

static uint32_t previous_value = 1u;
static uint32_t iteration;
static uint32_t expected_direction;
static uint32_t movement_seen;
static uint32_t num_correct;
static uint32_t num_wrong;

void exam_user_init(void)
{
  exam_joystick_start(exam_joystick_event);
  (void)exam_timer_every_ms(0, 3000, exam_timer_event);
}

void exam_user_loop(void)
{
}

void exam_timer_event(uint8_t timer, uint32_t flags)
{
  uint32_t remainder;

  if ((timer != 0u) || !exam_timer_match_happened(flags, 0u)) {
    return;
  }

  exam_leds_off();
  if (iteration >= 10u) {
    (void)exam_timer_stop(0u);
    if (num_correct > num_wrong) {
      (void)exam_led_on(4u);
    } else {
      (void)exam_led_on(5u);
    }
    return;
  }

  previous_value = nextElementLCG(previous_value, 131u, 7u,
                                  iteration, 255u);
  remainder = previous_value & 3u;

  movement_seen = 0u;
  if (remainder == 0u) {
    (void)exam_led_on(11u);
    expected_direction = EXAM_JOY_UP;
  } else if (remainder == 1u) {
    (void)exam_led_on(10u);
    expected_direction = EXAM_JOY_LEFT;
  } else if (remainder == 2u) {
    (void)exam_led_on(9u);
    expected_direction = EXAM_JOY_RIGHT;
  } else {
    (void)exam_led_on(8u);
    expected_direction = EXAM_JOY_DOWN;
  }

  iteration++;
}

void exam_joystick_event(uint32_t current, uint32_t changed)
{
  (void)changed;
  if (movement_seen || (current == 0u) || (iteration == 0u)) {
    return;
  }

  movement_seen = 1u;
  if (current & expected_direction) {
    num_correct++;
  } else {
    num_wrong++;
  }
  exam_leds_off();
}

void exam_user_10ms_hook(void)
{
}

/* Exam of 1 July 2025, ARM1, questions 1 to 3. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

/* Single-LED API arguments are physical board labels LD4 through LD11. */

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
static uint32_t previous_joystick;

void TIMER0_IRQHandler(void)
{
  uint32_t remainder;

  if ((exam_timer_ack(EXAM_TIMER0) & 1u) == 0u) {
    return;
  }

  exam_led_clear();
  if (iteration >= 10u) {
    exam_timer_stop(EXAM_TIMER0);
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

static void joystick_event(uint32_t pressed)
{
  if (movement_seen || (pressed == 0u) || (iteration == 0u)) {
    return;
  }

  movement_seen = 1u;
  if (pressed & expected_direction) {
    num_correct++;
  } else {
    num_wrong++;
  }
  exam_led_clear();
}

void RIT_IRQHandler(void)
{
  uint32_t current;
  uint32_t pressed;
  exam_rit_ack();
  current=exam_joystick_read();
  pressed=exam_joystick_pressed_edges(previous_joystick,current);
  previous_joystick=current;
  joystick_event(pressed);
}

int main(void)
{
  exam_init();
  exam_joystick_init();
  previous_joystick=exam_joystick_read();
  if(exam_rit_config_ms(10u)==EXAM_OK)exam_rit_start();
  if(exam_timer_config_ms(EXAM_TIMER0,3000u,EXAM_TIMER_PERIODIC)==EXAM_OK)
    exam_timer_start(EXAM_TIMER0);

  for (;;) {
    __WFI();
  }
}

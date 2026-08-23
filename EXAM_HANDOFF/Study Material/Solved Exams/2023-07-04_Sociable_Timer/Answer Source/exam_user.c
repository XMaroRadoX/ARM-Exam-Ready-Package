/* Exam of 4 July 2023, questions 1 and 2. */
#include "exam_user.h"

extern uint32_t isSociable(uint32_t number);

static const uint32_t numbers[7] = {
  8128u, 5564u, 5400u, 14264u, 1305184u, 1598470u, 4938136u
};

static uint32_t current_number;

void exam_user_init(void)
{
  /* 25 MHz / 25000 = 1000 timer counts per second. */
  (void)exam_timer_clock_divider(1u, 4u);
  (void)exam_timer_prescaler(1u, 24999u);
  (void)exam_timer_reset(1u);
  (void)exam_timer_match(1u, 0u, 2000u,
                         EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);
  (void)exam_timer_start(1u);
}

void exam_user_loop(void)
{
}

void TIMER1_IRQHandler(void)
{
  uint32_t pending = LPC_TIM1->IR & 0x3Fu;
  uint32_t result;

  LPC_TIM1->IR = pending;
  if ((pending & 1u) == 0u) {
    return;
  }

  result = isSociable(numbers[current_number]);
  current_number++;
  if (current_number == 7u) {
    current_number = 0u;
  }

  exam_leds_off();
  if ((result >= 1u) && (result <= 8u)) {
    (void)exam_led_on((uint8_t)(result + 3u));
  }
}

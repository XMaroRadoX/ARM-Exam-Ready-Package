/* Exam of 29 January 2025, ARM1, questions 1 and 2. */
#include "exam_user.h"

extern uint32_t bitwiseAffineTransformation(const uint8_t *matrix,
                                             uint32_t b,
                                             uint32_t c);

static const uint8_t transformation_matrix[8] = {
  0xF8u, 0x7Cu, 0x3Eu, 0x1Fu, 0x8Fu, 0xC7u, 0xE3u, 0xF1u
};

static uint8_t displayed_value;
static uint8_t blink_is_on;

void exam_user_init(void)
{
  /* Timer1 counts from 0 to 0xFFFF and resets without an interrupt. */
  (void)exam_timer_clock_divider(1u, 4u);
  (void)exam_timer_prescaler(1u, 0u);
  (void)exam_timer_reset(1u);
  (void)exam_timer_match(1u, 0u, 0xFFFFu, EXAM_TIMER_RESET);
  (void)exam_timer_start(1u);

  /* Timer0 uses 1000 counts per second when blinking is started. */
  (void)exam_timer_clock_divider(0u, 4u);
  (void)exam_timer_prescaler(0u, 24999u);
}

void exam_user_loop(void)
{
}

void EINT0_IRQHandler(void)
{
  uint32_t timer_value;
  uint32_t high_byte;
  uint32_t low_byte;

  LPC_SC->EXTINT = 1u;
  timer_value = exam_timer_count(1u) & 0xFFFFu;
  high_byte = (timer_value >> 8) & 0xFFu;
  low_byte = timer_value & 0xFFu;
  displayed_value = (uint8_t)(high_byte ^ low_byte);
  (void)exam_led_write(displayed_value);
}

void EINT1_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u << 1;

  displayed_value = (uint8_t)bitwiseAffineTransformation(
      transformation_matrix, displayed_value, 0x63u);

  blink_is_on = 1u;
  (void)exam_led_write(displayed_value);

  /* Toggle every 0.25 s, producing a complete 0.5 s blink period. */
  (void)exam_timer_stop(0u);
  (void)exam_timer_reset(0u);
  (void)exam_timer_match(0u, 0u, 250u,
                         EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);
  (void)exam_timer_start(0u);
}

void TIMER0_IRQHandler(void)
{
  uint32_t pending = LPC_TIM0->IR & 0x3Fu;

  LPC_TIM0->IR = pending;
  if ((pending & 1u) == 0u) {
    return;
  }

  blink_is_on ^= 1u;
  if (blink_is_on) {
    (void)exam_led_write(displayed_value);
  } else {
    exam_leds_off();
  }
}

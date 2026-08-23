/* Exam of 29 January 2025, ARM3, questions 1 and 2. */
#include "exam_user.h"

extern void transpose(const uint8_t *source, uint8_t *destination);

static uint8_t matrix_a[8];
static uint8_t matrix_b[8];
static uint8_t matrix_a_xor_b[8];
static uint8_t left_side[8];
static uint8_t transpose_a[8];
static uint8_t transpose_b[8];
static uint8_t right_side[8];
static uint32_t count_a;
static uint32_t count_b;

void exam_user_init(void)
{
  (void)exam_timer_clock_divider(2u, 4u);
  (void)exam_timer_prescaler(2u, 0u);
  (void)exam_timer_reset(2u);
  (void)exam_timer_match(2u, 0u, 0xFFFFu, EXAM_TIMER_RESET);
  (void)exam_timer_start(2u);
}

void exam_user_loop(void)
{
}

void EINT1_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u << 1;
  if (count_a < 8u) {
    matrix_a[count_a] = (uint8_t)exam_timer_count(2u);
    count_a++;
  }
}

void EINT2_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u << 2;
  if (count_b < 8u) {
    matrix_b[count_b] = (uint8_t)exam_timer_count(2u);
    count_b++;
  }
}

void EINT0_IRQHandler(void)
{
  uint32_t i;
  uint32_t equal = 1u;

  LPC_SC->EXTINT = 1u;
  if ((count_a < 8u) || (count_b < 8u)) {
    return;
  }

  for (i = 0u; i < 8u; i++) {
    matrix_a_xor_b[i] = matrix_a[i] ^ matrix_b[i];
  }

  transpose(matrix_a_xor_b, left_side);
  transpose(matrix_a, transpose_a);
  transpose(matrix_b, transpose_b);

  for (i = 0u; i < 8u; i++) {
    right_side[i] = transpose_a[i] ^ transpose_b[i];
    if (left_side[i] != right_side[i]) {
      equal = 0u;
    }
  }

  exam_leds_off();
  if (equal) {
    (void)exam_led_on(4u);
  } else {
    (void)exam_led_on(5u);
  }
}

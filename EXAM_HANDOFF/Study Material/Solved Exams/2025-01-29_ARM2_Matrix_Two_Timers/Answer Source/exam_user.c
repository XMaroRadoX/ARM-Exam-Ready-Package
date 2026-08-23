/* Exam of 29 January 2025, ARM2, questions 1 and 2. */
#include "exam_user.h"

extern void bitMatrixMultiplication(const uint8_t *matrix_a,
                                    const uint8_t *matrix_b,
                                    uint8_t *matrix_c);

static uint8_t matrix_a[8];
static uint8_t matrix_b[8];
static uint8_t matrix_c[8];
static uint32_t input_rows;
static uint32_t output_row;

void exam_user_init(void)
{
  (void)exam_timer_clock_divider(1u, 4u);
  (void)exam_timer_prescaler(1u, 0u);
  (void)exam_timer_reset(1u);
  (void)exam_timer_match(1u, 0u, 0xFFFFu, EXAM_TIMER_RESET);
  (void)exam_timer_start(1u);

  (void)exam_timer_clock_divider(0u, 4u);
  (void)exam_timer_prescaler(0u, 24999u);
}

void exam_user_loop(void)
{
}

void EINT0_IRQHandler(void)
{
  uint32_t value;

  LPC_SC->EXTINT = 1u;
  if (input_rows >= 8u) {
    return;
  }

  value = exam_timer_count(1u) & 0xFFFFu;
  matrix_a[input_rows] = (uint8_t)(value >> 8);
  matrix_b[input_rows] = (uint8_t)value;
  input_rows++;
}

void EINT1_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u << 1;
  if (input_rows < 8u) {
    return;
  }

  bitMatrixMultiplication(matrix_a, matrix_b, matrix_c);

  output_row = 1u;
  (void)exam_led_write(matrix_c[0]);

  (void)exam_timer_stop(0u);
  (void)exam_timer_reset(0u);
  (void)exam_timer_match(0u, 0u, 500u,
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

  if (output_row < 8u) {
    (void)exam_led_write(matrix_c[output_row]);
    output_row++;
  } else {
    exam_leds_off();
    (void)exam_timer_stop(0u);
    (void)exam_timer_reset(0u);
  }
}

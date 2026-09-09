/* Exam of 29 January 2025, ARM2, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

extern void bitMatrixMultiplication(const uint8_t *matrix_a,
                                    const uint8_t *matrix_b,
                                    uint8_t *matrix_c);

static uint8_t matrix_a[8];
static uint8_t matrix_b[8];
static uint8_t matrix_c[8];
static uint32_t input_rows;
static uint32_t output_row;

void EINT0_IRQHandler(void)
{
  uint32_t value;

  exam_button_ack(EXAM_BUTTON_INT0);
  if (input_rows >= 8u) {
    return;
  }

  value = exam_timer_read(EXAM_TIMER1) & 0xFFFFu;
  matrix_a[input_rows] = (uint8_t)(value >> 8);
  matrix_b[input_rows] = (uint8_t)value;
  input_rows++;
}

void EINT1_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY1);
  if (input_rows < 8u) {
    return;
  }

  bitMatrixMultiplication(matrix_a, matrix_b, matrix_c);

  output_row = 1u;
  (void)exam_led_write(matrix_c[0]);

  exam_timer_stop(EXAM_TIMER0);
  exam_timer_reset(EXAM_TIMER0);
  if (exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)==EXAM_OK)
    exam_timer_start(EXAM_TIMER0);
}

void TIMER0_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  if ((pending & 1u) == 0u) {
    return;
  }

  if (output_row < 8u) {
    (void)exam_led_write(matrix_c[output_row]);
    output_row++;
  } else {
    exam_led_clear();
    exam_timer_stop(EXAM_TIMER0);
    exam_timer_reset(EXAM_TIMER0);
  }
}

int main(void)
{
  exam_init();
  exam_buttons_init();
  if (exam_timer_config_ticks(EXAM_TIMER1,0xFFFFu,
                              EXAM_TIMER_MODULO_NO_IRQ)==EXAM_OK)
    exam_timer_start(EXAM_TIMER1);

  for (;;) {
    __WFI();
  }
}

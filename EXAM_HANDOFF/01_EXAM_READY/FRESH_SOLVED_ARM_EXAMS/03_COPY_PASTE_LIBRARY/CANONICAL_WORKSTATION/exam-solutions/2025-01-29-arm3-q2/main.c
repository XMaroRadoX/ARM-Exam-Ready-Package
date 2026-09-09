/* Exam of 29 January 2025, ARM3, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

/* Single-LED API arguments are physical board labels LD4 through LD11. */

extern void transposition(const uint8_t *source, uint8_t *destination);

static uint8_t matrix_a[8];
static uint8_t matrix_b[8];
static uint8_t matrix_a_xor_b[8];
static uint8_t left_side[8];
static uint8_t transpose_a[8];
static uint8_t transpose_b[8];
static uint8_t right_side[8];
static uint32_t count_a;
static uint32_t count_b;

void EINT1_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY1);
  if (count_a < 8u) {
    matrix_a[count_a] = (uint8_t)exam_timer_read(EXAM_TIMER2);
    count_a++;
  }
}

void EINT2_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY2);
  if (count_b < 8u) {
    matrix_b[count_b] = (uint8_t)exam_timer_read(EXAM_TIMER2);
    count_b++;
  }
}

void EINT0_IRQHandler(void)
{
  uint32_t i;
  uint32_t equal = 1u;

  exam_button_ack(EXAM_BUTTON_INT0);
  if ((count_a < 8u) || (count_b < 8u)) {
    return;
  }

  for (i = 0u; i < 8u; i++) {
    matrix_a_xor_b[i] = matrix_a[i] ^ matrix_b[i];
  }

  transposition(matrix_a_xor_b, left_side);
  transposition(matrix_a, transpose_a);
  transposition(matrix_b, transpose_b);

  for (i = 0u; i < 8u; i++) {
    right_side[i] = transpose_a[i] ^ transpose_b[i];
    if (left_side[i] != right_side[i]) {
      equal = 0u;
    }
  }

  exam_led_clear();
  if (equal) {
    (void)exam_led_on(4u);
  } else {
    (void)exam_led_on(5u);
  }
}

int main(void)
{
  exam_init();
  exam_buttons_init();
  if (exam_timer_config_ticks(EXAM_TIMER2,0xFFFFu,
                              EXAM_TIMER_MODULO_NO_IRQ)==EXAM_OK)
    exam_timer_start(EXAM_TIMER2);

  for (;;) {
    __WFI();
  }
}

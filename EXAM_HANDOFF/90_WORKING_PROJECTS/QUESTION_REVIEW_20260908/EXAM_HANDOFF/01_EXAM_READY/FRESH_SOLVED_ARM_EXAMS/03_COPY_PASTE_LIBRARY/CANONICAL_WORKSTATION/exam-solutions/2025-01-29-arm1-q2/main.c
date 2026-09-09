/* Exam of 29 January 2025, ARM1, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

extern uint32_t bitwiseAffineTransformation(const uint8_t *matrix,
                                             uint32_t b,
                                             uint32_t c);

static const uint8_t transformation_matrix[8] = {
  0x8Fu, 0xC7u, 0xE3u, 0xF1u, 0xF8u, 0x7Cu, 0x3Eu, 0x1Fu
};

static uint8_t displayed_value;
static uint8_t blink_is_on;

void EINT0_IRQHandler(void)
{
  uint32_t timer_value;
  uint32_t high_byte;
  uint32_t low_byte;

  exam_button_ack(EXAM_BUTTON_INT0);
  timer_value = exam_timer_read(EXAM_TIMER1) & 0xFFFFu;
  high_byte = (timer_value >> 8) & 0xFFu;
  low_byte = timer_value & 0xFFu;
  displayed_value = (uint8_t)(high_byte ^ low_byte);
  (void)exam_led_write(displayed_value);
}

void EINT1_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY1);

  displayed_value = (uint8_t)bitwiseAffineTransformation(
      transformation_matrix, displayed_value, 0x63u);

  blink_is_on = 1u;
  (void)exam_led_write(displayed_value);

  /* Toggle every 0.25 s, producing a complete 0.5 s blink period. */
  exam_timer_stop(EXAM_TIMER0);
  exam_timer_reset(EXAM_TIMER0);
  if (exam_timer_config_ms(EXAM_TIMER0,250u,EXAM_TIMER_PERIODIC)==EXAM_OK)
    exam_timer_start(EXAM_TIMER0);
}

void TIMER0_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  if ((pending & 1u) == 0u) {
    return;
  }

  blink_is_on ^= 1u;
  if (blink_is_on) {
    (void)exam_led_write(displayed_value);
  } else {
    exam_led_clear();
  }
}

int main(void)
{
  exam_init();
  exam_buttons_init();
  /* Timer1 counts from 0 to 0xFFFF and resets without an interrupt. */
  if (exam_timer_config_ticks(EXAM_TIMER1,0xFFFFu,
                              EXAM_TIMER_MODULO_NO_IRQ)==EXAM_OK)
    exam_timer_start(EXAM_TIMER1);

  for (;;) {
    __WFI();
  }
}

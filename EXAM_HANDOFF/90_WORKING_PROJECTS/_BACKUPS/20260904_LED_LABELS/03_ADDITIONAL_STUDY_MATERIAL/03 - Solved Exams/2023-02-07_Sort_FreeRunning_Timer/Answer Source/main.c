/* Exam of 7 February 2023, questions 1 and 2. */
#include <stdint.h>
#include "LPC17xx.h"

/* Physical LED label = 11 - API index (P2 bit). */
#include "exam_api.h"

#define MAX_VALUES 20u

extern void copyData(const int8_t *source, int8_t *destination,
                     uint32_t length);
extern void insertionSort(int8_t *values, uint32_t length);

static int8_t values[MAX_VALUES];
static uint32_t value_count;
static uint32_t show_led6 = 1u;

void EINT0_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_INT0);

  if (value_count < MAX_VALUES) {
    values[value_count] = (int8_t)exam_timer_read(EXAM_TIMER1);
    value_count++;

    if (show_led6) {
      (void)exam_led_on(5u);  /* physical LED6 */
      (void)exam_led_off(4u); /* physical LED7 */
    } else {
      (void)exam_led_off(5u);
      (void)exam_led_on(4u);
    }
    show_led6 ^= 1u;
  }
}

void EINT1_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY1);
  (void)exam_led_off(5u);
  (void)exam_led_off(4u);
  insertionSort(values, value_count);
  (void)exam_led_on(0u); /* physical LED11 */
}

int main(void)
{
  exam_init();
  exam_buttons_init();
  /* Timer1 resets at 0xFF, but its match does not generate an interrupt. */
  (void)exam_timer_config_ticks(EXAM_TIMER1, 0xFFu,
                                EXAM_TIMER_MODULO_NO_IRQ);
  exam_timer_start(EXAM_TIMER1);

  for (;;) {
    __WFI();
  }
}

#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

/* Single-LED API arguments are physical board labels LD4 through LD11. */

extern uint32_t digitSum(uint32_t value);
extern uint32_t digitaddition(uint32_t *area, uint32_t count);

static uint32_t series[10];
static volatile uint32_t entered_value;

static void handle_button(exam_button_t button)
{
  uint32_t reported;
  uint32_t formula;
  if (button == EXAM_BUTTON_KEY1) {
    entered_value <<= 1;        /* append binary digit 0 */
  } else if (button == EXAM_BUTTON_KEY2) {
    entered_value = (entered_value << 1) | 1u;
  } else if (button == EXAM_BUTTON_INT0) {
    series[0] = entered_value;
    reported = digitaddition(series, 10u);
    /* Zero seed legitimately generates ten zeroes. Other zero returns mean
       overflow and leave the tail incomplete, so do not read that tail. */
    formula = (reported || series[0] == 0u)
      ? series[9] - series[0] + digitSum(series[9]) : UINT32_MAX;
    if (reported == formula) {
      (void)exam_led_on(4u);
      (void)exam_led_off(5u);
    } else {
      (void)exam_led_off(4u);
      (void)exam_led_on(5u);
    }
  }
}

void EINT0_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_INT0); handle_button(EXAM_BUTTON_INT0); }
void EINT1_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_KEY1); handle_button(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_KEY2); handle_button(EXAM_BUTTON_KEY2); }

int main(void)
{
  exam_init();
  entered_value = 0u;
  exam_led_clear();
  exam_buttons_init();

  for (;;) {
    __WFI();
  }
}

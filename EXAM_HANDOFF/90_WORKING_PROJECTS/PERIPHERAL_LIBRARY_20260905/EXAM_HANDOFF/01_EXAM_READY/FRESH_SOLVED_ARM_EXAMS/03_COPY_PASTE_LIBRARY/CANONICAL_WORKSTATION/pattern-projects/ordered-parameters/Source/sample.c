#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t step, increment, offset, result;
void command(uint32_t identity) {
  if (step == 0u) { increment=identity+2u; step=1u; }
  else { offset=identity; result=increment*10u+offset; exam_led_write((uint8_t)result);step=0u; }
}
void EINT0_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_INT0);command(0u); }
void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1);command(1u); }
void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2);command(2u); }
int main(void) {
  exam_init();exam_buttons_init();
  NVIC_SetPriority(EINT0_IRQn,2u);NVIC_SetPriority(EINT1_IRQn,2u);NVIC_SetPriority(EINT2_IRQn,2u);
  for (;;) {}
}

#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t entered, bit_count, result;
/* Equal priorities prevent these handlers interrupting one another.
 * Hardware cannot reconstruct chronology of edges already pending together;
 * in that case the NVIC vector ordering decides. */
void EINT1_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_KEY1);
  if (bit_count < 32u) { entered <<= 1; ++bit_count; }
}
void EINT2_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_KEY2);
  if (bit_count < 32u) { entered = (entered << 1) | 1u; ++bit_count; }
}
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  result=entered; exam_led_write((uint8_t)result);
  entered=0u;bit_count=0u;
}
int main(void) {
  exam_init(); exam_buttons_init();
  NVIC_SetPriority(EINT0_IRQn,2u);NVIC_SetPriority(EINT1_IRQn,2u);NVIC_SetPriority(EINT2_IRQn,2u);
  for (;;) {}
}

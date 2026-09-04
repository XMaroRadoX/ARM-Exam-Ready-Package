#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t captured;
void EINT0_IRQHandler(void) {
  captured = exam_timer_read(EXAM_TIMER1);
  exam_button_ack(EXAM_BUTTON_INT0);
  exam_led_write((uint8_t)captured);
}
int main(void) {
  exam_init(); exam_buttons_init();
  require(exam_timer_config_ticks(EXAM_TIMER1, 0xFFFFu, EXAM_TIMER_MODULO_NO_IRQ));
  exam_timer_start(EXAM_TIMER1);
  for (;;) {}
}

void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1); }

void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2); }

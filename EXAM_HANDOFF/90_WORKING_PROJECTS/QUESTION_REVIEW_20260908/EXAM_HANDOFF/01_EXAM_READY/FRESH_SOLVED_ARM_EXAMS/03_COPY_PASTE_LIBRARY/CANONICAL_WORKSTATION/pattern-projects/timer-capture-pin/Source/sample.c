#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t last_capture, capture_count;
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_capture_happened(flags,0u)) { last_capture=LPC_TIM0->CR0; ++capture_count; }
}
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0,UINT32_MAX,EXAM_TIMER_MODULO_NO_IRQ));
  require(exam_timer_config_match(EXAM_TIMER0,0u,UINT32_MAX,0u));
  /* P1.26 function 3 is CAP0.0; capture TC on rising edges and interrupt. */
  LPC_PINCON->PINSEL3=(LPC_PINCON->PINSEL3 & ~(3u<<20)) | (3u<<20);
  LPC_GPIO1->FIODIR &= ~(1u<<26);
  LPC_TIM0->CCR=(LPC_TIM0->CCR & ~7u) | 5u;
  (void)exam_timer_ack(EXAM_TIMER0);NVIC_ClearPendingIRQ(TIMER0_IRQn);
  NVIC_EnableIRQ(TIMER0_IRQn);exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}

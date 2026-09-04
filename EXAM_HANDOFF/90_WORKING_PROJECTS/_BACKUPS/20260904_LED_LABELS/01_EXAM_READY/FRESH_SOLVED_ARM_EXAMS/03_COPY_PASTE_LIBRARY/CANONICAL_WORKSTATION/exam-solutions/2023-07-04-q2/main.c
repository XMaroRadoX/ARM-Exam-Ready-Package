/* Exam of 4 July 2023, questions 1 and 2. */
#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t isSociable(uint32_t number);

static const uint32_t numbers[7] = {
  8128u, 5564u, 5400u, 14264u, 1305184u, 1598470u, 4938136u
};

static uint32_t current_number;

void TIMER1_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER1);
  uint32_t result;

  if ((pending & 1u) == 0u) {
    return;
  }

  result = isSociable(numbers[current_number]);
  current_number++;
  if (current_number == 7u) {
    current_number = 0u;
  }

  exam_led_clear();
  if ((result >= 1u) && (result <= 8u)) {
    /* result 1 -> physical LED4 (index 7); result 8 -> LED11 (index 0). */
    (void)exam_led_on((uint8_t)(8u - result));
  }
}

int main(void)
{
  exam_init();
  (void)exam_timer_config_ms(EXAM_TIMER1, 2000u, EXAM_TIMER_PERIODIC);
  exam_timer_start(EXAM_TIMER1);

  for (;;) {
    __WFI();
  }
}

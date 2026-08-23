/* Exam of 7 February 2023, questions 1 and 2. */
#include "exam_user.h"

#define MAX_VALUES 20u

extern void copyData(const int8_t *source, int8_t *destination,
                     uint32_t length);
extern void insertionSort(int8_t *values, uint32_t length);

static int8_t values[MAX_VALUES];
static uint32_t value_count;
static uint32_t show_led6 = 1u;

void exam_user_init(void)
{
  /* Timer1 resets at 0xFF, but its match does not generate an interrupt. */
  (void)exam_timer_clock_divider(1u, 4u);
  (void)exam_timer_prescaler(1u, 0u);
  (void)exam_timer_reset(1u);
  (void)exam_timer_match(1u, 0u, 0xFFu, EXAM_TIMER_RESET);
  (void)exam_timer_start(1u);
}

void exam_user_loop(void)
{
}

void EINT0_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u;

  if (value_count < MAX_VALUES) {
    values[value_count] = (int8_t)exam_timer_count(1u);
    value_count++;

    if (show_led6) {
      (void)exam_led_on(6u);
      (void)exam_led_off(7u);
    } else {
      (void)exam_led_off(6u);
      (void)exam_led_on(7u);
    }
    show_led6 ^= 1u;
  }
}

void EINT1_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u << 1;
  (void)exam_led_off(6u);
  (void)exam_led_off(7u);
  insertionSort(values, value_count);
  (void)exam_led_on(11u);
}

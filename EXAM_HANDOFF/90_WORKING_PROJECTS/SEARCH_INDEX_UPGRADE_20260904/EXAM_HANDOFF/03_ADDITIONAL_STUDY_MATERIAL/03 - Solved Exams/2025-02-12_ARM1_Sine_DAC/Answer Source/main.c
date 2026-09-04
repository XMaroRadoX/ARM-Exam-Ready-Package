/* Exam of 12 February 2025, ARM1, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

extern int32_t Maclaurin(int32_t y, uint32_t order);

int sineValues[45];
static int repeat_count;
static int ticks;
static uint32_t started;

void EINT0_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_INT0);
  if (started) {
    return;
  }
  started = 1u;

  if (exam_timer_config_ticks(EXAM_TIMER0,1263u,
                              EXAM_TIMER_PERIODIC)==EXAM_OK)
    exam_timer_start(EXAM_TIMER0);
}

void TIMER0_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  float scaled_input;
  int input;
  int output;

  if ((pending & 1u) == 0u) {
    return;
  }

  if (repeat_count < 200) {
    scaled_input = 1.428f * (float)ticks;
    input = (int)(scaled_input + ((scaled_input >= 0.0f) ? 0.5f : -0.5f));
    output = 500 + Maclaurin(input, 3u) / 2;
    sineValues[ticks + 22] = output;
    (void)exam_dac_write(output);

    ticks++;
    if (ticks > 22) {
      ticks = -22;
      repeat_count++;
    }
  } else {
    (void)exam_dac_write(0);
    exam_timer_stop(EXAM_TIMER0);
  }
}

int main(void)
{
  exam_init();
  exam_buttons_init();
  exam_dac_init();

  for (;;) {
    __WFI();
  }
}

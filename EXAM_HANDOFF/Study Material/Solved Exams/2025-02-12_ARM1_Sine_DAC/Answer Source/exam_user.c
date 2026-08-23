/* Exam of 12 February 2025, ARM1, questions 1 and 2. */
#include "exam_user.h"

extern int32_t Maclaurin(int32_t y, uint32_t order);

int sineValues[45];
static int repeat_count;
static int ticks;
static uint32_t started;

void exam_user_init(void)
{
  (void)exam_timer_clock_divider(0u, 4u);
  (void)exam_timer_prescaler(0u, 0u);
}

void exam_user_loop(void)
{
}

void EINT0_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u;
  if (started) {
    return;
  }
  started = 1u;

  (void)exam_timer_reset(0u);
  (void)exam_timer_match(0u, 0u, 1263u,
                         EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);
  (void)exam_timer_start(0u);
}

void TIMER0_IRQHandler(void)
{
  uint32_t pending = LPC_TIM0->IR & 0x3Fu;
  float scaled_input;
  int input;
  int output;

  LPC_TIM0->IR = pending;
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
    exam_dac_silence();
    (void)exam_timer_stop(0u);
  }
}

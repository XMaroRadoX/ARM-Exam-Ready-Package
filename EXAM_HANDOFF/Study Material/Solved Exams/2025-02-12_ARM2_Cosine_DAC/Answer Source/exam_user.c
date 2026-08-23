/* Exam of 12 February 2025, ARM2, questions 1 and 2. */
#include "exam_user.h"

extern int32_t Maclaurin_cos(int32_t y, uint32_t order);

int cosineValues[45];
static int repeat_count;
static int ticks;
static uint32_t started;

void exam_user_init(void)
{
  (void)exam_timer_clock_divider(1u, 4u);
  (void)exam_timer_prescaler(1u, 0u);
}

void exam_user_loop(void)
{
}

void EINT1_IRQHandler(void)
{
  LPC_SC->EXTINT = 1u << 1;
  if (started) {
    return;
  }
  started = 1u;

  (void)exam_timer_reset(1u);
  (void)exam_timer_match(1u, 0u, 1592u,
                         EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);
  (void)exam_timer_start(1u);
}

void TIMER1_IRQHandler(void)
{
  uint32_t pending = LPC_TIM1->IR & 0x3Fu;
  float scaled_input;
  int input;
  int output;

  LPC_TIM1->IR = pending;
  if ((pending & 1u) == 0u) {
    return;
  }

  if (repeat_count < 200) {
    scaled_input = 1.428f * (float)ticks;
    input = (int)(scaled_input + ((scaled_input >= 0.0f) ? 0.5f : -0.5f));
    output = 500 + Maclaurin_cos(input, 3u) / 2;
    cosineValues[ticks + 22] = output;
    (void)exam_dac_write(output);

    ticks++;
    if (ticks > 22) {
      ticks = -22;
      repeat_count++;
    }
  } else {
    exam_dac_silence();
    (void)exam_timer_stop(1u);
  }
}

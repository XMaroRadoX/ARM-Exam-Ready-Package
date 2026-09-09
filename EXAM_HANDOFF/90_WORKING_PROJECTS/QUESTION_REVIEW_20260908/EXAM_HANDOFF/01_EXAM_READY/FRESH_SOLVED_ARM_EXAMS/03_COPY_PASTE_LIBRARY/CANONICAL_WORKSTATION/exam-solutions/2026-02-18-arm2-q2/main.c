/* Exam of 18 February 2026, ARM2, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

#define SEQUENCE_LENGTH 1000u
#define SAMPLE_COUNT      45u

extern uint32_t HofstadterConway(uint32_t *values, int dimension);

static uint32_t sequence[SEQUENCE_LENGTH];
static uint32_t sequence_maximum;
static uint32_t sequence_index;
static uint32_t sample_index = SAMPLE_COUNT - 1u;

static const uint16_t SinTable[SAMPLE_COUNT] = {
  410, 467, 523, 576, 627, 673, 714, 749, 778,
  799, 813, 819, 817, 807, 789, 764, 732, 694,
  650, 602, 550, 495, 438, 381, 324, 270, 217,
  169, 125, 87, 55, 30, 12, 2, 0, 6, 20, 41,
  70, 105, 146, 193, 243, 297, 353
};

/* Evaluate the paper's formula in floating point, then cast the result. */
static uint32_t note_threshold(uint32_t value,
                               uint32_t maximum_period,
                               uint32_t minimum_period,
                               uint32_t k)
{
  float range_per_step;
  float threshold;

  range_per_step = (float)(maximum_period - minimum_period) /
                   (float)sequence_maximum;
  threshold = ((float)maximum_period - range_per_step * (float)value) /
              (float)k;

  if (threshold < 1.0f) {
    threshold = 1.0f;
  }

  return (uint32_t)threshold;
}

/* Timer A: choose and start the next note when B and C are both stopped. */
void TIMER0_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  uint32_t value;
  uint32_t waveform_threshold;
  uint32_t duration_threshold;

  if ((pending & 1u) == 0u) {
    return;
  }

  if (sequence_index >= SEQUENCE_LENGTH ||
      exam_timer_is_running(EXAM_TIMER1) ||
      exam_timer_is_running(EXAM_TIMER2)) {
    return;
  }

  value = sequence[sequence_index];
  waveform_threshold = note_threshold(value, 5351u, 1062u, 1u);
  duration_threshold = note_threshold(value, 40000000u, 625000u, 5u);

  sequence_index++;
  if (sequence_index == SEQUENCE_LENGTH) {
    (void)exam_timer_stop(EXAM_TIMER0);
  }

  /* Timer B resets on every match and therefore remains periodic. */
  (void)exam_timer_stop(EXAM_TIMER1);
  (void)exam_timer_reset(EXAM_TIMER1);
  (void)exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                                EXAM_TIMER_PERIODIC);

  /* Timer C is a one-shot: interrupt, reset and stop at the match. */
  (void)exam_timer_stop(EXAM_TIMER2);
  (void)exam_timer_reset(EXAM_TIMER2);
  (void)exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                                EXAM_TIMER_ONE_SHOT);

  (void)exam_timer_start(EXAM_TIMER1);
  (void)exam_timer_start(EXAM_TIMER2);
}

/* Timer B: send the next sinusoidal sample to the DAC. */
void TIMER1_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER1);
  if ((pending & 1u) == 0u) {
    return;
  }

  if (!exam_timer_is_running(EXAM_TIMER1)) return;
  sample_index++;
  if (sample_index == SAMPLE_COUNT) {
    sample_index = 0u;
  }

  (void)exam_dac_write(SinTable[sample_index]);
}

/* Timer C: terminate the note by stopping Timer B. */
void TIMER2_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER2);
  if ((pending & 1u) == 0u) {
    return;
  }

  (void)exam_timer_stop(EXAM_TIMER1);
  (void)exam_timer_reset(EXAM_TIMER1);
  (void)exam_timer_stop(EXAM_TIMER2);
  (void)exam_timer_reset(EXAM_TIMER2);
  (void)exam_dac_write(0);
}

int main(void)
{
  exam_init();
  exam_dac_init();
  sequence_maximum = HofstadterConway(sequence, (int)SEQUENCE_LENGTH);
  (void)exam_dac_write(0);

  /* The Combined API derives 50 ms from Timer0's actual peripheral clock. */
  (void)exam_timer_config_ms(EXAM_TIMER0, 50u, EXAM_TIMER_PERIODIC);
  (void)exam_timer_start(EXAM_TIMER0);

  for (;;) {
    /* This paper places the required work in the three timer handlers. */
    __WFI();
  }
}

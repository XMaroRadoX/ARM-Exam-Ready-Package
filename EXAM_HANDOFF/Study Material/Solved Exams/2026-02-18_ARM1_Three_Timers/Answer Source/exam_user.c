/* Exam of 18 February 2026, ARM1, questions 1 and 2. */
#include "exam_user.h"

#define SEQUENCE_LENGTH 1000u
#define SAMPLE_COUNT      45u

extern uint32_t HofstadterQ(uint32_t *values, int dimension);

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

void exam_user_init(void)
{
  sequence_maximum = HofstadterQ(sequence, (int)SEQUENCE_LENGTH);
  exam_dac_silence();

  /* All three counters receive 25 MHz: 100 MHz CCLK divided by four. */
  (void)exam_timer_clock_divider(0u, 4u); /* Timer A: scheduler. */
  (void)exam_timer_clock_divider(1u, 4u); /* Timer B: waveform.  */
  (void)exam_timer_clock_divider(2u, 4u); /* Timer C: duration.  */
  (void)exam_timer_prescaler(0u, 0u);
  (void)exam_timer_prescaler(1u, 0u);
  (void)exam_timer_prescaler(2u, 0u);

  /* Timer A interrupts every 50 ms: 25,000,000 * 0.050. */
  (void)exam_timer_reset(0u);
  (void)exam_timer_match(0u, 0u, 1250000u,
                         EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);
  (void)exam_timer_start(0u);
}

void exam_user_loop(void)
{
  /* This paper places the required work in the three timer handlers. */
}

/* Timer A: choose and start the next note when B and C are both stopped. */
void TIMER0_IRQHandler(void)
{
  uint32_t pending = LPC_TIM0->IR & 0x3Fu;
  uint32_t value;
  uint32_t waveform_threshold;
  uint32_t duration_threshold;

  LPC_TIM0->IR = pending;
  if ((pending & 1u) == 0u) {
    return;
  }

  if ((LPC_TIM1->TCR & 1u) || (LPC_TIM2->TCR & 1u)) {
    return;
  }

  value = sequence[sequence_index];
  waveform_threshold = note_threshold(value, 5351u, 1062u, 1u);
  duration_threshold = note_threshold(value, 40000000u, 625000u, 5u);

  sequence_index++;
  if (sequence_index == SEQUENCE_LENGTH) {
    (void)exam_timer_stop(0u);
  }

  /* Timer B resets on every match and therefore remains periodic. */
  (void)exam_timer_stop(1u);
  (void)exam_timer_reset(1u);
  (void)exam_timer_match(1u, 0u, waveform_threshold,
                         EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);

  /* Timer C is a one-shot: interrupt, reset and stop at the match. */
  (void)exam_timer_stop(2u);
  (void)exam_timer_reset(2u);
  (void)exam_timer_match(2u, 0u, duration_threshold,
                         EXAM_TIMER_INTERRUPT |
                         EXAM_TIMER_RESET |
                         EXAM_TIMER_STOP);

  (void)exam_timer_start(1u);
  (void)exam_timer_start(2u);
}

/* Timer B: send the next sinusoidal sample to the DAC. */
void TIMER1_IRQHandler(void)
{
  uint32_t pending = LPC_TIM1->IR & 0x3Fu;

  LPC_TIM1->IR = pending;
  if ((pending & 1u) == 0u) {
    return;
  }

  sample_index++;
  if (sample_index == SAMPLE_COUNT) {
    sample_index = 0u;
  }

  (void)exam_dac_write((int)SinTable[sample_index]);
}

/* Timer C: terminate the note by stopping Timer B. */
void TIMER2_IRQHandler(void)
{
  uint32_t pending = LPC_TIM2->IR & 0x3Fu;

  LPC_TIM2->IR = pending;
  if ((pending & 1u) == 0u) {
    return;
  }

  (void)exam_timer_stop(1u);
  (void)exam_timer_reset(1u);
  (void)exam_timer_stop(2u);
  (void)exam_timer_reset(2u);
  exam_dac_silence();
}

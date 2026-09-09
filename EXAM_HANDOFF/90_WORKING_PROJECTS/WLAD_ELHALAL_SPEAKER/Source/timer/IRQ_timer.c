#include "LPC17xx.h"
#include "timer.h"
#include "exam_api.h"
#include "song_decoder.h"

/*
 * exam_timer_ack() snapshots and clears every active timer flag before it
 * returns. Test the saved snapshot for each source used by the question:
 * bit 0 MR0, bit 1 MR1, bit 2 MR2, bit 3 MR3, bit 4 CR0, bit 5 CR1.
 *
 * Example for a Timer0 question that also enables MR1:
 *   if ((pending & (1u << 1)) != 0u) {
 *     // Write the question-specific MR1 action here.
 *   }
 *
 * Keep all enabled sources in this one handler; do not define a duplicate
 * TIMERn_IRQHandler in another file.
 */
/* One audio sample per interrupt; reset the board to replay. */
void TIMER0_IRQHandler(void)
{
    static uint32_t position = 0;
    uint32_t pending = exam_timer_ack(EXAM_TIMER0);

    if (exam_timer_match_happened(pending, 0))
    {
        if (position < SONG_SAMPLE_COUNT)
        {
            exam_dac_write((song_next_sample() + 32768) >> 6);
            position++;
        }
        else
        {
            exam_timer_stop(EXAM_TIMER0);
            exam_dac_write(512);
            exam_led_off(4);
            exam_led_on(5);
        }
    }
}

void TIMER1_IRQHandler (void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER1);
  if ((pending & (1u << 0)) != 0u) {
    /* Write the question-specific Timer1 action here. */
  }
}

void TIMER2_IRQHandler (void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER2);
  if ((pending & (1u << 0)) != 0u) {
    /* Write the question-specific Timer2 action here. */
  }
}

void TIMER3_IRQHandler (void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER3);
  if ((pending & (1u << 0)) != 0u) {
    /* Write the question-specific Timer3 action here. */
  }
}

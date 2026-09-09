#include "LPC17xx.h"
#include "timer.h"
#include "exam_api.h"

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






void TIMER3_IRQHandler (void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER3);
  if ((pending & (1u << 0)) != 0u) {
    /* Write the question-specific Timer3 action here. */
  }
}

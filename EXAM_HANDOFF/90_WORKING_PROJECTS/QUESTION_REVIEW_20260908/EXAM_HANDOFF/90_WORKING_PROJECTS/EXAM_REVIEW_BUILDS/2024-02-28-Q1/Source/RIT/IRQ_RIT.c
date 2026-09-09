#include "LPC17xx.h"
#include "RIT.h"
#include "exam_api.h"

void RIT_IRQHandler (void)
{
  exam_rit_ack();
  /* Call exam_debounce_tick() here when RIT is the debounce time source. */
  /* Write the question-specific RIT action here. */
}

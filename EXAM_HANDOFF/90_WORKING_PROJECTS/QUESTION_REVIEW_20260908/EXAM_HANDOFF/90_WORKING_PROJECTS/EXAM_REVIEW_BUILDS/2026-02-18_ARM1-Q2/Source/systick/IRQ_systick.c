#include "LPC17xx.h"
#include "systick.h"
#include "exam_api.h"

void SysTick_Handler (void)
{
  /* SysTick is acknowledged automatically by the Cortex-M processor. */
  /* Call exam_debounce_tick() here when SysTick is the debounce time source. */
  /* Write the question-specific SysTick action here. */
}

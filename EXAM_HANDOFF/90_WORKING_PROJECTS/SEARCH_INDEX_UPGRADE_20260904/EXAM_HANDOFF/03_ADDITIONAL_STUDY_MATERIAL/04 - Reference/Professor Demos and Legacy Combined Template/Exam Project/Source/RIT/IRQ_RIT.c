#include "LPC17xx.h"
#include "RIT.h"

void RIT_IRQHandler (void)
{
  LPC_RIT->RICTRL |= 0x1;
}

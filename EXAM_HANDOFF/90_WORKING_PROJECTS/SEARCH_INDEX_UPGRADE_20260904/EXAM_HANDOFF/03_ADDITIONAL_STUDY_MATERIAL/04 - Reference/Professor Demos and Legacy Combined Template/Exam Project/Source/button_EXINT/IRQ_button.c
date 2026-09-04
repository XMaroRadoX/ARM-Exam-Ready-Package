#include "LPC17xx.h"
#include "button.h"

void EINT0_IRQHandler (void)
{
  LPC_SC->EXTINT = (1 << 0);
}

void EINT1_IRQHandler (void)
{
  LPC_SC->EXTINT = (1 << 1);
}

void EINT2_IRQHandler (void)
{
  LPC_SC->EXTINT = (1 << 2);
}

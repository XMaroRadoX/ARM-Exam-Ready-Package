#include "LPC17xx.h"
#include "timer.h"

void TIMER0_IRQHandler (void)
{
  LPC_TIM0->IR = 1;
}

void TIMER1_IRQHandler (void)
{
  LPC_TIM1->IR = 1;
}

#ifndef MOCK_LPC_H
#define MOCK_LPC_H
#include <stdint.h>
#define __WFI() ((void)0)
#define TIMER0_IRQn 1
#define TIMER1_IRQn 2
#define RIT_IRQn 3
void NVIC_SetPriority(int,uint32_t);
#endif

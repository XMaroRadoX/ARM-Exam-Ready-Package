#pragma once
#include <stdint.h>
#define TIMER0_IRQn 1
#define RIT_IRQn 29
void NVIC_SetPriority(int,uint32_t);
void __WFI(void);

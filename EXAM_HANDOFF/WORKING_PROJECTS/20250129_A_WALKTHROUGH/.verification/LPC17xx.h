
#ifndef MOCK_LPC
#define MOCK_LPC
#include <stdint.h>
typedef enum { EINT0_IRQn, EINT1_IRQn, EINT2_IRQn, RIT_IRQn, TIMER0_IRQn, TIMER1_IRQn } IRQn_Type;
static inline void __disable_irq(void) {}
static inline void __enable_irq(void) {}
static inline void __WFI(void) {}
static inline void NVIC_DisableIRQ(IRQn_Type x) { (void)x; }
static inline void NVIC_ClearPendingIRQ(IRQn_Type x) { (void)x; }
static inline void NVIC_SetPriority(IRQn_Type x, uint32_t p) { (void)x; (void)p; }
#endif

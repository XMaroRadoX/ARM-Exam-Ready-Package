#include "LPC17xx.h"
#include "adc.h"

/*----------------------------------------------------------------------------
  Function that initializes ADC
 *----------------------------------------------------------------------------*/
void ADC_init (void) {

  LPC_PINCON->PINSEL3  =  (LPC_PINCON->PINSEL3 & ~(3UL << 30)) |
                           (3UL << 30); /* P1.31 is AD0.5                     */

  LPC_SC->PCONP       |=  (1<<12);      /* Enable power to ADC block          */

  /* PCLK_ADC = CCLK/4. At 100 MHz and CLKDIV=4, ADC clock = 5 MHz. */
  LPC_SC->PCLKSEL0    &= ~(3UL << 24);

  LPC_ADC->ADCR        =  (1<< 5) |     /* select AD0.5 pin                   */
                          (4<< 8) |     /* ADC clock is 25MHz/5               */
                          (1<<21);      /* enable ADC                         */ 

  LPC_ADC->ADINTEN     =  (1<< 8);      /* global enable interrupt            */

  NVIC_ClearPendingIRQ(ADC_IRQn);       /* discard stale pending state         */
  NVIC_EnableIRQ(ADC_IRQn);             /* enable ADC Interrupt               */
}

void ADC_start_conversion (void) {
	LPC_ADC->ADCR = (LPC_ADC->ADCR & ~(7UL << 24)) |
	                 (1UL << 24);         /* software-triggered conversion      */
}

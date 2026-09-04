#include "LPC17xx.h"
#include "adc.h"

void ADC_IRQHandler (void)
{
  (void)LPC_ADC->ADGDR;
}

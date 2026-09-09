#include "LPC17xx.h"
#include "adc.h"
#include "exam_api.h"

void ADC_IRQHandler (void)
{
  exam_adc_irq_capture();
  /* The result can be taken safely in main with exam_adc_take(). */
}

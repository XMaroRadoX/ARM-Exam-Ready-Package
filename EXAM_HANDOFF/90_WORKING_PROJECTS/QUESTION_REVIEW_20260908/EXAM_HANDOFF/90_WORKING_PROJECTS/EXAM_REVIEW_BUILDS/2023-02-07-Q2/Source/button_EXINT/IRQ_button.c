#include "LPC17xx.h"
#include "button.h"
#include "exam_api.h"





void EINT2_IRQHandler (void)
{
  exam_button_ack(EXAM_BUTTON_KEY2);
  /* For a debounced question, replace the line above with:
     exam_debounce_begin(EXAM_BUTTON_KEY2); */
}

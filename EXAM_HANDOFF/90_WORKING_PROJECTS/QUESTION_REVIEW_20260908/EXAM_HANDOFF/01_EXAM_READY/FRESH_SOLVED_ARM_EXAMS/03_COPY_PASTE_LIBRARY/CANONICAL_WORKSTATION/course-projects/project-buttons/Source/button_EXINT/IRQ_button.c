#include "exam_api.h"

void EINT0_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_INT0); }
void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2); }

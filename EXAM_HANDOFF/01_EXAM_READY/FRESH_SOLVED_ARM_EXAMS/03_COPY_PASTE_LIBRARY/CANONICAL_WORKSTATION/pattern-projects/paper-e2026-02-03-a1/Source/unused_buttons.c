#include "exam_api.h"
/* Acknowledge enabled buttons unused by this paper. The answer source is unchanged. */
void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2); }

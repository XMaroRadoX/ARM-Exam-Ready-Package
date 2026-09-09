#include "LPC17xx.h"
#include "exam_api.h"

void EINT0_IRQHandler(void)
{
    exam_button_ack(EXAM_BUTTON_INT0);

    /* This exam requires only the first press to have an effect. */
    NVIC_DisableIRQ(EINT0_IRQn);

    exam_timer_start(EXAM_TIMER0);
}

void EINT1_IRQHandler(void)
{
    exam_button_ack(EXAM_BUTTON_KEY1);
}

void EINT2_IRQHandler(void)
{
    exam_button_ack(EXAM_BUTTON_KEY2);
}

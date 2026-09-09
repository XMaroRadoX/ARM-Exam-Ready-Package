#include "LPC17xx.h"
#include "exam_api.h"

extern int Maclaurin(int y, int n);

/* Required by the paper: global, 45 elements, in IRQ_timer.c. */
int sineValues[45];

void TIMER0_IRQHandler(void)
{
    static int repeat = 0;
    static int ticks = 0;
    int input;
    int output;
    float scaled;
    uint32_t pending;

    pending = exam_timer_ack(EXAM_TIMER0);
    if ((pending & 1u) == 0u)
    {
        return;
    }

    if (repeat < 200)
    {
        scaled = 1.428f * ticks;

        if (scaled >= 0.0f)
        {
            input = (int)(scaled + 0.5f);
        }
        else
        {
            input = (int)(scaled - 0.5f);
        }

        output = 500 + Maclaurin(input, 3) / 2;
        sineValues[ticks + 22] = output;

        /* The DAC sample occupies bits 15:6; BIAS remains zero. */
        LPC_DAC->DACR = (uint32_t)output << 6;

        ticks++;
        if (ticks > 22)
        {
            ticks = -22;
            repeat++;
        }
    }
    else
    {
        /* Preserve the paper's behavior: keep writing zero afterward. */
        LPC_DAC->DACR = 0u;
    }
}

void TIMER1_IRQHandler(void)
{
    (void)exam_timer_ack(EXAM_TIMER1);
}

void TIMER2_IRQHandler(void)
{
    (void)exam_timer_ack(EXAM_TIMER2);
}

void TIMER3_IRQHandler(void)
{
    (void)exam_timer_ack(EXAM_TIMER3);
}

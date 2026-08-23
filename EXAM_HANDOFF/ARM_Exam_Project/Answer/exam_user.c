#include "exam_user.h"

/* The core clock, LED pins and fault support are ready before this function.
 * Timers, input devices, ADC, DAC, RIT and SysTick remain available but off. */
void exam_user_init(void)
{
}

/* Foreground application processing. */
void exam_user_loop(void)
{
}

/* Optional bounded task called by the platform's 10 ms service. */
void exam_user_10ms_hook(void)
{
}

# Question 2: complete three-second LED answer

## Put each complete file in the working template

| Download | Destination |
|---|---|
| main.c | Source/sample.c |
| assembly.s | Source/ASM_funct.s |
| IRQ_timer.c | Source/timer/IRQ_timer.c |

The complete C answer includes TIMER0_IRQHandler so it is readable in one file. The provided IRQ_timer.c retains Timer1-3 and omits only the duplicate Timer0 handler. Replace files rather than appending a second handler. This changes placement only; it is the same timer/LED solution.

Keep the template's original startup file. Replace Q1's custom reset assembly with this callable-only assembly so normal Reset_Handler enters C main.

## What happens every three seconds

The timer handler acknowledges the MR0 interrupt, calls nextElementLCG once, selects the LED using 11 - (value % 4), clears the old LED, and turns on the new one. Static previous and n retain their values between interrupts.

The C compiler passes previous/a/c/n in R0-R3 and the fifth argument on the stack. The returned R0 becomes value.

| Remainder | LED |
|---|---|
| 0 | 11 |
| 1 | 10 |
| 2 | 9 |
| 3 | 8 |

Expected LED order: 9, 9, 8, 8, 11, 8, 9, 9, 9, 10.

The first LED appears at approximately 3 seconds. After the tenth call at approximately 30 seconds, Timer0 stops and LED10 stays on. No joystick or RIT is needed for Q2.

## Common mistakes

Do not restart previous or n on every interrupt. Do not call the assembly function from a fast foreground loop. Do not leave the old LED on. Do not pass low-level LED indexes to helpers that expect physical labels.

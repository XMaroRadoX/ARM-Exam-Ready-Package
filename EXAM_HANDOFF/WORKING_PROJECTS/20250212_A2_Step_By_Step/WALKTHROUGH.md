# 12 February 2025, A2: complete worked solution

This practice project solves both questions in the supplied 20250212.pdf.
It was copied from the current Official Combined Exam API starting template.
The original template was not edited.

## Start here

Open sample.uvprojx in Keil. The four solution files are already included.
Do not add a second copy of the assembly function or interrupt handlers.

1. Source/ASM_funct.s implements Question 1.
2. Source/sample.c initializes the board, DAC and stopped timer.
3. Source/button_EXINT/IRQ_button.c starts Timer 0 on the first INT0 press.
4. Source/timer/IRQ_timer.c implements the required sample generation and stores sineValues.

The supplied startup code and board libraries remain part of the project.
The exam_api functions used below are existing functions in this template.

## High-level explanation

A sine wave is a repeated smooth rise and fall. A DAC (digital-to-analog
converter) turns a number into a voltage. Sending successive sine-wave
samples to the DAC at regular times produces the voltage waveform used by
the board's speaker circuit.

Question 1 calculates one approximate sine value using integer arithmetic.
Question 2 repeatedly calls that function to create an audio waveform.

Execution order:

main initializes everything -> waits for an interrupt.
First INT0 press -> EINT0_IRQHandler starts Timer 0.
Every 1263 timer clock cycles -> TIMER0_IRQHandler calculates and outputs one sample.
After repeat reaches 200 -> later timer interrupts write zero.

An interrupt temporarily pauses the current code and runs a specially
named handler. The startup file connects those names to the processor's
interrupt table. You do not call the handlers from main.

## Question 1: mathematics

The input y represents ten times the angle in radians: x = y / 10.
The returned integer approximates 100*sin(y/10). The paper's sin(y)
wording is inconsistent with its own scaling and example.

Calculate terms t0 through tn, including both ends:

t0 = 10*y
ti = (-previous_term*y*y) / ((2*i)*(2*i+1)*100)

Start total at t0. For i from 1 through n, compute the complete numerator
and denominator, divide once using signed integer division, and add the
new term to total. Return total.

For y=20 and n=3:

| i | Numerator | Denominator | Term | Total |
|---|---:|---:|---:|---:|
| 0 | - | - | 200 | 200 |
| 1 | -80000 | 600 | -133 | 67 |
| 2 | 53200 | 2000 | 26 | 93 |
| 3 | -10400 | 4200 | -2 | 91 |

Integer division truncates toward zero: -133.333 becomes -133.
Do not use unsigned division or round the intermediate terms to nearest.
The nearest-integer rule in Question 2 applies to the angle conversion only.

## Question 1: assembly explanation

The C calling convention puts y in R0 and n in R1. Return the result in R0.
R0-R3 are scratch registers; R4-R7 must be restored because they belong to
the caller.

| Register | Use |
|---|---|
| R0 | y on entry, answer on return |
| R1 | n |
| R2 | y squared |
| R3 | current term, temporarily its numerator |
| R4 | running total |
| R5 | i |
| R6 | denominator |
| R7 | temporary factor |

PUSH saves R4-R7 and the return address LR on the stack.
MUL R2,R0,R0 means R2=R0*R0.
MOV copies a number or another register's value. The # prefix means a literal.
CMP R5,R1 compares i with n. BGT finished exits only when i is greater.
RSB R3,R3,#0 means R3=0-R3, which changes the sign.
SDIV R3,R3,R6 divides the signed numerator by the denominator.
ADD R4,R4,R3 adds the new term to the running total.
B next_term jumps back to the loop check.
MOV R0,R4 places the answer where the C caller expects it.
POP restores saved registers and loads the saved return address into PC,
which returns execution to the caller.

The function calls no other function. If it is later changed to call one,
also review stack alignment at the new call boundary.

For n=0 the initial i=1 is already greater than n, so return t0 immediately.
This code assumes the exam's intended input range and nonnegative n.

## Question 2: initialization

exam_init initializes the existing board support and system clock.
exam_dac_init selects P0.26 as AOUT and starts the DAC at zero with BIAS=0.
exam_timer_config_ticks configures Timer 0 but leaves it stopped:
- timer mode, rather than external pulse counting;
- prescaler PR=0, one timer count per peripheral clock cycle;
- match register MR0=1263;
- interrupt and reset on match (MCR bits 0 and 1 set);
- timer counter cleared;
- Timer 0 interrupt enabled.

exam_timer_set_clock_divider sets the timer peripheral clock to core/4.
The current template configures a 100 MHz core clock, so Timer 0 uses 25 MHz.

sample rate = 25,000,000 / 1263 = 19,794.14 samples/second
full-cycle frequency = sample rate / 45 = 439.87 Hz
sample interval = 1263 / 25,000,000 = 50.52 microseconds

These are timer peripheral clock cycles, not CPU instruction counts.
With the same 1263 value but a different clock divider, the pitch changes.

Initialize buttons last so a press cannot start an unprepared timer.
The infinite main loop uses __WFI to wait for interrupts.

The (void) casts explicitly discard status return values. Here the calls
use fixed valid arguments on the freshly initialized template.

## Question 2: first button press

exam_button_ack clears the INT0 peripheral interrupt flag.
NVIC_DisableIRQ disables future INT0 handler entries. The first press
starts playback and later presses cannot restart it. No debounce routine
or debounce timer is required for this paper.
exam_timer_start sets Timer 0's TCR to 1.

The KEY1 and KEY2 handlers only acknowledge their own events because those
buttons have no assigned action in this exam.

## Question 2: timer handler, line by line

The global declaration int sineValues[45] is outside all functions in
IRQ_timer.c, exactly where the paper requires it.

static int repeat=0 and static int ticks=0 are initialized only once and
retain their values between interrupts. Ordinary local variables would
restart at zero on each call and the waveform would never advance.

exam_timer_ack returns and clears active Timer 0 interrupt flags.
The test pending & 1u checks bit 0, corresponding to MR0. If it is absent,
return without generating a sample. Acknowledgement clears the interrupt
request; it does not stop the timer.

For repeat<200:

1. scaled=1.428f*ticks converts the position into a scaled angle.
   The suffix f requests single-precision floating-point arithmetic.
2. For a nonnegative value add 0.5 before casting to int; for a negative
   value subtract 0.5 before casting. C's cast discards the fractional part.
   For example 2.856 becomes 3, and -2.856 becomes -3.
3. Call Maclaurin(input,3), which includes t0,t1,t2,t3.
4. Divide that returned integer by 2 and add 500.
5. Store the output at sineValues[ticks+22].
6. Write the output shifted left six bits into DACR.
7. Increment ticks. If it exceeds 22, set ticks=-22 and increment repeat.

The approximate scaling is:
Maclaurin returns about 100*sin(angle).
Dividing by 2 gives about 50*sin(angle).
Adding 500 gives a wave centered at 500, with amplitude about 50.

For ticks=14:
scaled=19.992 -> input=20 -> Maclaurin=91 -> 91/2=45 -> output=545.
The index is 14+22=36, so sineValues[36]=545.
The register word is 545<<6=34880.

For ticks=-14:
input=-20 -> Maclaurin=-91 -> -91/2=-45 -> output=455.
The index is 8. This division truncates toward zero.

The DAC is 10 bits, accepting values 0..1023. Its sample field is bits
15:6, so shifting left by six positions places the number in that field.
The shift does not multiply the intended analog amplitude. A fresh register
assignment replaces the previous sample; |= would incorrectly retain old bits.
This project uses BIAS=0, so writing the complete register with zero in
the other fields is intentional.

## Indexing and the first partial pass

| ticks | array index |
|---:|---:|
| -22 | 0 |
| -1 | 21 |
| 0 | 22 |
| 1 | 23 |
| 22 | 44 |

There are 45 integer positions from -22 to 22 inclusive.
The +22 converts each signed position into a valid array index.

The paper explicitly starts ticks at 0. The first pass is therefore
0,1,...,22: 23 samples, filling indexes 22..44.
All later passes are -22,-21,...,22: 45 samples.
Do not change the initialization to -22 just to make all passes equal.

After each sample at ticks=22, the code wraps ticks to -22 and increments
repeat. The loop generates 23+199*45=8978 computed samples before repeat
reaches 200. On interrupt 8979 it writes zero, and subsequent interrupts
continue writing zero, matching the paper.

The first complete 45-element array is available after the negative half
of the second pass has been generated. The array stores the most recently
written value at each position; it is not a recording of all 8978 samples.

## Short trace

| ticks | input | Maclaurin | output | index |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 500 | 22 |
| 1 | 1 | 10 | 505 | 23 |
| 2 | 3 | 30 | 515 | 24 |
| 11 | 16 | 100 | 550 | 33 |
| 14 | 20 | 91 | 545 | 36 |
| 22 | 31 | -2 | 499 | 44 |
| -22 | -31 | 2 | 501 | 0 |
| -14 | -20 | -91 | 455 | 8 |
| -11 | -16 | -100 | 450 | 11 |

The endpoint values differ from an exact sine because this is a truncated,
integer approximation. Preserve the specified recurrence.

## Practical steps in Keil

1. Open this copy's sample.uvprojx.
2. Build the desired target.
3. For Question 1 alone, temporarily call Maclaurin(20,3) from main and
   inspect its returned value (91). Use an extern declaration in that file.
4. For Question 2 inspect Timer 0 after initialization: PR=0, MR0=1263,
   MCR low bits=3, TCR=0.
5. Press INT0: TCR becomes 1.
6. Inspect sineValues in the debugger, with values approximately 450..550.
7. Check the first outputs and wrap against the trace above.
8. Check repeat reaches 200 and DACR subsequently becomes zero.
9. Press INT0 again: it does not restart playback.

Breakpoints interrupt real-time playback. Use them to inspect state; test
the actual sound with the program running freely on the correctly connected board.

## Common mistakes

- Stopping at i>=n rather than i>n skips the last required term.
- Starting total at zero without adding t0 omits the first term.
- UDIV mishandles negative values.
- Dividing intermediate factors too early changes integer rounding.
- Rounding Question 2's negative angles by adding 0.5 gives wrong results.
- Removing static restarts playback state at every interrupt.
- Using sineValues[ticks] accesses negative indexes.
- Starting Timer 0 in main plays before the button press.
- Forgetting acknowledgement leaves an interrupt request active.
- Writing output directly into DACR places it in the wrong bit positions.
- Changing ticks=0 to ticks=-22 changes the specified initial sequence.
- Making repeat count samples instead of wraps changes playback duration.

## Possible practice variations

These are exercises, not predictions about the next exam:
- Change n: change the number of terms in Question 1.
- Change pitch: change the timer sample period while keeping 45 positions.
- Allow replay: reset ticks/repeat and re-enable the button, with explicit
  ownership of shared state and a debounce policy if the new question needs one.
- Change volume: adjust the sine amplitude while keeping the DAC range valid.

## Verification scope

See build_SW_Debug.log and build_LandTiger.log for compiler/linker results.
verify_math.py checks the paper example, negative and zero inputs, all 45
rounded inputs, DAC range, array bounds and the exact initial/end sequence.
math_check.json contains all sample values.

Build success and the reference arithmetic model do not prove audible
playback, simulator execution, or interrupt timing on the physical board.
The physical board has not been tested.

## Sources

- Original exam: 02_ORIGINAL_MATERIALS/Exams/ARM questions/20250212.pdf,
  pages 1-2, A2 Questions 1 and 2.
- Current source template: 01_EXAM_READY/02_STARTING_TEMPLATES/Official
  Combined Exam API, including Source/exam_api/exam_api.c and .h,
  Source/system_LPC17xx.c and sample.uvprojx.
- NXP LPC17xx User Manual UM10360: timer and DAC register descriptions.
- ARM Cortex-M3 Devices Generic User Guide: signed division semantics.

## Complete code

### Source/ASM_funct.s

```asm
        AREA    Maclaurin_Code, CODE, READONLY
        THUMB
        EXPORT  Maclaurin

; int Maclaurin(int y, int n)
; R0: y on entry, answer on return. R1: nonnegative n.
; R2: y*y. R3: current term. R4: total. R5: i.
; R6: denominator. R7: temporary value.

Maclaurin PROC
        PUSH    {R4-R7, LR}

        MUL     R2, R0, R0      ; y squared
        MOV     R3, #10
        MUL     R3, R0, R3      ; t0 = 10*y
        MOV     R4, R3          ; total = t0
        MOV     R5, #1          ; first new term has index 1

next_term
        CMP     R5, R1
        BGT     finished       ; stop when i > n

        MUL     R3, R3, R2
        RSB     R3, R3, #0      ; numerator = -previous_term*y*y

        ADD     R6, R5, R5      ; 2*i
        ADD     R7, R6, #1      ; 2*i + 1
        MUL     R6, R6, R7
        MOV     R7, #100
        MUL     R6, R6, R7      ; denominator = (2*i)*(2*i+1)*100

        SDIV    R3, R3, R6      ; signed division, truncate toward zero
        ADD     R4, R4, R3      ; add new term
        ADD     R5, R5, #1
        B       next_term

finished
        MOV     R0, R4
        POP     {R4-R7, PC}
        ENDP
        END
```

### Source/sample.c

```c
#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
    exam_init();
    exam_dac_init();

    /* Configure Timer 0, but leave it stopped until INT0 is pressed. */
    (void)exam_timer_config_ticks(EXAM_TIMER0, 1263u,
                                  EXAM_TIMER_PERIODIC);

    /* Template core clock: 100 MHz. Timer clock: 100/4 = 25 MHz. */
    (void)exam_timer_set_clock_divider(EXAM_TIMER0, 4u);

    /* Enable buttons after the DAC and timer are ready. */
    exam_buttons_init();

    while (1)
    {
        __WFI();
    }
}
```

### Source/button_EXINT/IRQ_button.c

```c
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
```

### Source/timer/IRQ_timer.c

```c
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
```



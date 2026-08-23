# Ultimate ARM exam navigator

This guide is the operating procedure for the exam. Follow it in order when
stressed. It tells you what to read, what to decide, which code shape to use,
what to test and what not to submit.

## 0. Know the two boundaries

On the USB drive, the sibling folder `ARM_Exam_Project` is the clean Keil
project. `Study Material` is the private reference library containing
this guide.

At the start of the exam:

1. Copy `ARM_Exam_Project` to a writable location on the exam computer.
2. Keep the original USB copy unchanged as a recovery copy.
3. Open `ARM_Exam_Template.uvprojx` from the copied folder.
4. Build immediately. The untouched baseline must produce zero errors and zero
   warnings before any answer is written.
5. Normally edit only `Answer/exam_user.c` and
   `Answer/exam_asm.s`.

If the baseline does not build, do not start changing algorithm code. Confirm
that the project was copied completely, the `CA Exam` target is selected and
Arm Compiler 6 is available.

## 1. Translate the paper into a contract

Before coding, write a small contract on paper or at the top of the answer:

```text
Q1 function name:
arguments and registers:
return register/value:
element width and signedness:
array/matrix dimensions:
may modify input memory? yes/no:
must call another routine? yes/no:
flags part of output? yes/no:

Q2 input events:
timers and periods:
shared variables:
foreground work:
ISR-only work:
output LEDs/DAC/array:
```

Underline exact words such as `byte`, `word`, `signed`, `unsigned`, `at most`,
`until`, `including`, `handler`, `without interrupts`, `reset on match`, and
`return flags`. These words determine instructions and loop boundaries.

Do not infer a missing requirement from an old exam. Use an old solution only
after matching its contract to the new paper.

## 2. Classify Q1 assembly in under two minutes

Use the first matching row. Several rows may apply.

| Wording or shape | Family | Open next |
|---|---|---|
| sort, reorder, minimum, maximum | sorting/nested loops | [sorting](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-SORTING-001.md) |
| next term, sequence, repeat until constant | recurrence/fixed point | [recurrence](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-RECURRENCE-001.md) |
| maze, graph, neighbor, shortest path, DFS | graph search/matrix | [graph search](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-GRAPH-SEARCH-001.md) |
| count repeated values/digits | frequency count | [frequency count](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-FREQUENCY-COUNT-001.md) |
| byte array or characters | byte memory | [byte arrays](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-BYTE-ARRAY-001.md) |
| int/word array | word memory | [word arrays](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-WORD-ARRAY-001.md) |
| matrix `[row][column]` | row-major address | [matrix addressing](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-MATRIX-ROW-MAJOR-001.md) |
| calls helper or contains `BL` | non-leaf ABI | [non-leaf calls](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-NONLEAF-001.md) |
| five or more arguments | stacked arguments | [stacked arguments](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-STACKED-ARGS-001.md) |
| SVC or exception | exception frame | [SVC](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-SVC-001.md) |
| N/Z/C/V are outputs | flag-sensitive routine | [flags](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-FLAGS-001.md) |

For a broader wording search, open the
[quick pattern lookup](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/QUICK_PATTERN_LOOKUP.md).

## 3. Build the assembly frame before the algorithm

### Leaf function using only R0-R3 and R12

```asm
                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  required_function

required_function PROC
                ; R0-R3 are caller-saved. No push is needed if no preserved
                ; register is used and this routine never executes BL.
                ; ... calculation ...
                BX      LR
                ENDP
                ALIGN   4
                END
```

### Non-leaf function

```asm
required_function PROC
                PUSH    {R4-R6, LR}    ; four registers: SP stays 8-byte aligned
                MOV     R4, R0         ; preserve values needed after BL
                MOV     R5, R1
                BL      helper
                ; R0-R3 and flags may have changed; R4/R5 remain valid.
                POP     {R4-R6, PC}
                ENDP
```

Save LR before the first `BL`. Preserve every used register from R4 through
R11. Push an even number of registers when calling another public function so
SP remains eight-byte aligned.

### Five or more parameters

Stacked arguments are relative to the caller's SP, before your push:

```asm
required_function PROC
                MOV     R12, SP
                PUSH    {R4-R8, LR}    ; 24 bytes, still 8-byte aligned
                LDR     R4, [R12]      ; argument 5
                LDR     R5, [R12, #4]  ; argument 6
                LDR     R6, [R12, #8]  ; argument 7
                ; arguments 1-4 are still in R0-R3
                ; ...
                POP     {R4-R8, PC}
                ENDP
```

Never calculate stacked offsets after pushing unless the push size is included
in the calculation. Capturing original SP first is less error-prone.

## 4. Choose correct memory instructions

| Data in paper | Load | Store | Index scale |
|---|---|---|---:|
| unsigned byte/char | `LDRB` | `STRB` | 1 |
| signed byte | `LDRSB` | `STRB` | 1 |
| unsigned halfword | `LDRH` | `STRH` | 2 |
| signed halfword | `LDRSH` | `STRH` | 2 |
| 32-bit int/word | `LDR` | `STR` | 4 |

Common forms:

```asm
; byte[i]
LDRB    R3, [R0, R2]

; word[i]
LDR     R3, [R0, R2, LSL #2]

; byte matrix[row][col], address = base + row * columns + col
MUL     R3, R1, R2          ; R1=row, R2=columns
ADD     R3, R3, R4          ; R4=column
LDRB    R5, [R0, R3]

; word matrix[row][col]
MUL     R3, R1, R2
ADD     R3, R3, R4
LDR     R5, [R0, R3, LSL #2]
```

If multiplication is prohibited, replace `MUL` with the exact allowed shift,
addition or repeated-addition method. Do not silently violate the paper.

## 5. Construct loops without overruns

### Counted loop

```asm
                MOVS    R2, #0
loop_check      CMP     R2, R1
                BHS     loop_done      ; unsigned i >= length
                LDRB    R3, [R0, R2]
                ; process element
                ADDS    R2, R2, #1
                B       loop_check
loop_done
```

For a neighbor access `array[i+1]`, stop at `i < length-1`. For an interior
matrix scan, rows are `1 .. rows-2` and columns are `1 .. columns-2`. Test the
empty/minimum case before subtracting one from an unsigned length.

### Nested row/column loop

```asm
                MOVS    R4, #0          ; row
row_check       CMP     R4, R1
                BHS     rows_done
                MOVS    R5, #0          ; column must reset for each row
col_check       CMP     R5, R2
                BHS     next_row
                ; index = row * columns + column
                MUL     R6, R4, R2
                ADD     R6, R6, R5
                ; process [R0 + R6]
                ADDS    R5, R5, #1
                B       col_check
next_row        ADDS    R4, R4, #1
                B       row_check
rows_done
```

## 6. Handle signedness and flags deliberately

- Unsigned compare: `BLO/BHS/BHI/BLS`.
- Signed compare: `BLT/BGE/BGT/BLE`.
- `CMP` performs a subtraction only for flags; it does not store a result.
- `ADDS/SUBS` update flags; plain `ADD/SUB` may be preferable when flags must
  survive.
- To detect signed addition overflow immediately: branch with `BVS` after
  `ADDS` before another flag-setting instruction.
- To detect unsigned carry: use `BCS` after `ADDS`.
- A nested `BL` may destroy caller-saved registers and flags.

If N/Z/C/V are part of the returned contract, arrange the final flag-setting
instruction at the end or modify APSR exactly as allowed by the question.

## 7. SVC and exception scenario

The hardware frame is R0, R1, R2, R3, R12, LR, PC, xPSR. Select MSP or PSP
from exception LR, then decode the byte before stacked PC:

```asm
SVC_Handler     PROC
                TST     LR, #4
                ITE     EQ
                MRSEQ   R0, MSP
                MRSNE   R0, PSP
                LDR     R1, [R0, #24]   ; stacked return PC
                LDRB    R2, [R1, #-2]   ; SVC immediate
                ; dispatch R2; stacked R0 is [R0,#0]
                BX      LR
                ENDP
```

If the paper explicitly guarantees MSP, that assumption may simplify the
answer, but the generic form is safer. Ensure only one linked file owns
`SVC_Handler`; duplicate vector symbols cause linker errors.

## 8. Classify Q2 C/peripheral work

| Requirement | Preferred project API |
|---|---|
| set/display LEDs | `exam_led_write`, `exam_led_on`, `exam_led_off`, `exam_led_toggle` |
| INT0/KEY events with debounce | `exam_buttons_start(callback)` |
| inspect current button state | `exam_button_pressed` or `exam_buttons_pressed` |
| joystick events | `exam_joystick_start(callback)` |
| periodic timer | `exam_timer_every_ms` or `exam_timer_every_hz` |
| free-running random seed/time | prescaler + reset + `exam_timer_start`, then `exam_timer_count` |
| direct match configuration | `exam_timer_match` |
| ADC/potentiometer | `exam_pot_start`, `exam_pot_read`, `exam_adc_read` |
| DAC | `exam_dac_write`, `exam_dac_percent`, `exam_dac_silence` |
| foreground event handoff | `exam_events_set`, `exam_events_take` |

The full declarations are in the submission project's
`Source/platform/exam_api.h`. For old professor names such as `LED_On`,
`init_timer`, or `init_RIT`, include `exam_compat.h`.

## 9. Canonical event-driven C shape

```c
#include "exam_user.h"

extern uint32_t required_function(uint32_t *data, uint32_t length);

static volatile exam_button_t last_button;
static volatile uint32_t last_timer_flags;

void exam_user_init(void)
{
    exam_leds_off();
    (void)exam_buttons_start(exam_button_event);
    (void)exam_timer_every_ms(0, 500, exam_timer_event);
}

void exam_user_loop(void)
{
    uint32_t pending = exam_events_take(EXAM_EVENT_BUTTON |
                                        EXAM_EVENT_TIMER);

    if ((pending & EXAM_EVENT_BUTTON) != 0u) {
        exam_button_t button = last_button;
        /* Perform longer algorithm/state work here. */
        (void)button;
    }

    if ((pending & EXAM_EVENT_TIMER) != 0u) {
        uint32_t flags = last_timer_flags;
        /* Advance one scheduled output step here. */
        (void)flags;
    }
}

void exam_button_event(exam_button_t button, exam_button_event_t event)
{
    if (event == EXAM_PRESS) {
        last_button = button;
        exam_events_set(EXAM_EVENT_BUTTON);
    }
}

void exam_timer_event(uint8_t timer, uint32_t flags)
{
    (void)timer;
    last_timer_flags = flags;
    exam_events_set(EXAM_EVENT_TIMER);
}

void exam_user_10ms_hook(void)
{
}
```

Objects written in callbacks/interrupt context and read in foreground must be
`volatile`. If multiple fields must be read consistently, take a short critical
section, copy them locally, then leave the critical section before doing work.

## 10. Common Q2 scenarios

### Button builds a binary number

```c
if (button == EXAM_BUTTON_KEY1) {
    value <<= 1;                 /* append 0 */
} else if (button == EXAM_BUTTON_KEY2) {
    value = (value << 1) | 1u;   /* append 1 */
} else if (button == EXAM_BUTTON_INT0) {
    run_requested = 1u;
}
```

Decide what happens when 32 bits are already present. If the paper is silent,
use a count and stop accepting digits at 32 rather than invoking undefined
behavior or silently losing important input.

### Two-button/two-stage state machine

```c
typedef enum { WAIT_FIRST, WAIT_SECOND, READY } input_state_t;
static volatile input_state_t state;
static uint32_t first_value;
static uint32_t second_value;

/* In foreground after a confirmed press: */
if (state == WAIT_FIRST) {
    first_value = decode_button(button);
    state = WAIT_SECOND;
} else if (state == WAIT_SECOND) {
    second_value = decode_button(button);
    state = READY;
}
```

Keep button-to-number mapping in one `decode_button` function. That makes a
paper correction a one-function change.

### Periodic LED sequence

Store the sequence and current index globally. Let each timer event perform one
step; do not busy-wait for 500 ms inside a callback.

```c
static const uint8_t led_for_direction[4] = {4u, 5u, 6u, 7u};
static volatile uint32_t step_due;

/* timer callback */
step_due = 1u;
exam_events_set(EXAM_EVENT_TIMER);

/* foreground */
if (step_due != 0u) {
    step_due = 0u;
    exam_leds_off();
    exam_led_on(led_for_direction[path[position]]);
    ++position;
}
```

If the required presentation alternates 0.5 s on and 0.5 s off, model `ON` and
`OFF` as explicit states instead of assuming every timer tick means a new LED.

### Free-running timer used as seed

```c
(void)exam_timer_prescaler(0u, 0u);
(void)exam_timer_reset(0u);
(void)exam_timer_start(0u);

/* Later, on the required event: */
seed = exam_timer_count(0u);
```

Do not configure reset-on-match for a timer intended to run freely. If the
question says “without interrupts,” do not use `exam_timer_every_ms`; configure
and start the counter without an interrupt match.

### ADC controls a value

```c
int sample;
if (exam_pot_read(&sample) == EXAM_OK) {
    /* sample is valid; map it using the paper's exact range/formula. */
}
```

Check whether the formula needs the raw 12-bit ADC value, a percentage, a
threshold or a table index. Clamp the resulting index before accessing a table.

### DAC waveform

```c
static const uint16_t waveform[] = {512u, 700u, 900u, 700u,
                                    512u, 324u, 124u, 324u};
static uint32_t wave_index;

exam_dac_write((int)waveform[wave_index]);
wave_index = (wave_index + 1u) %
             (sizeof waveform / sizeof waveform[0]);
```

Use the exact table, sample period and wrap behavior in the paper. DAC samples
are 10-bit; keep values in 0..1023.

## 11. When direct handlers are required

Use the high-level callback API unless the question explicitly tests register
configuration or names an IRQ handler. When writing the exact handler:

1. Enable the matching `EXAM_OWN_*_HANDLER` switch in `exam_config.h`.
2. Read pending flags once.
3. Clear only those pending flags, using the peripheral's write-one-to-clear
   rule.
4. Capture minimal state or perform the exact short action required.
5. Return. Do not sort, search a maze, or run a long recurrence inside an ISR
   unless the paper explicitly requires that location.

```c
void TIMER0_IRQHandler(void)
{
    uint32_t pending = LPC_TIM0->IR;
    LPC_TIM0->IR = pending;
    last_timer_flags = pending;
    exam_events_set(EXAM_EVENT_TIMER);
}
```

One vector has one owner. A duplicate `TIMER0_IRQHandler`, `RIT_IRQHandler`,
`SysTick_Handler`, or `SVC_Handler` is a linker/design error.

## 12. Connect C and assembly correctly

The C prototype must exactly represent the register contract:

```c
extern uint32_t sum_bytes(const uint8_t *data, uint32_t length);
extern int32_t signed_result(int32_t value);
extern uint64_t wide_result(uint32_t input); /* returned in R0:R1 */
```

Checklist:

- Assembly symbol spelling equals C prototype spelling, including case.
- Assembly has `EXPORT symbol`.
- Pointer type matches element width.
- Signed types match signed loads/comparisons.
- Return type matches R0 or R0:R1 behavior.
- The `.s` file is included in the Keil project group.

## 13. Test in a deliberate order

After each meaningful block, build. Do not write the entire answer before the
first compile.

### Assembly vector set

Test at least:

1. The example printed in the paper.
2. Minimum legal size/value.
3. Maximum configured size/value.
4. Empty or zero only if allowed.
5. Duplicate/repeated values.
6. Already sorted/already finished input.
7. Signed negative and positive cases when signed.
8. Boundary that makes a loop run exactly once.

Place recognizable guard words before and after output arrays while debugging:

```c
uint32_t before = 0xA5A5A5A5u;
uint8_t output[32];
uint32_t after = 0x5A5A5A5Au;
```

After the call, both guards must be unchanged.

### Peripheral sequence set

Mentally or in the simulator walk through:

- press, release, bounce and repeated press;
- two buttons in both possible orders;
- timer fires before/after a button;
- timer repeats after stop/restart;
- last array/table element wraps to zero;
- ADC minimum, midpoint and maximum;
- foreground is delayed while another event arrives.

## 14. Debug by symptom

| Symptom | First checks |
|---|---|
| linker says multiply defined handler | two files own the same vector; inspect `EXAM_OWN_*` switches |
| linker cannot find assembly function | spelling, `EXPORT`, project inclusion, prototype |
| returns correctly once, fails on second call | R4-R11 or LR not preserved; SP not restored |
| crashes after `BL` | LR not saved or SP misaligned |
| wrong matrix row | used rows instead of columns in `row * columns + col` |
| works for bytes under 128 only | signed/unsigned load mismatch |
| last element corrupted | `<= length` instead of `< length`, or wrong element scale |
| button appears multiple times | no debounce or acting on both press and release |
| timer runs at wrong speed | peripheral clock/divider/prescaler/match calculation |
| interrupt repeats forever | pending flag not cleared correctly |
| foreground misses state | non-volatile shared state or non-atomic multi-field read |
| DAC noise/wrong pitch | sample period, table wrap, 10-bit scaling, timer ownership |

For a complete guided practice session, use the
[Bulls and Cows debug lab](../Practice%20Projects/BULLS_AND_COWS_DEBUG_LAB/DEBUG_AND_LEARN.md).

## 15. Recovery plan when stuck

1. Re-read only the function contract and one printed example.
2. Reduce the algorithm to pseudocode with explicit loop bounds.
3. Confirm byte/word and signed/unsigned decisions.
4. Restore a known-good prologue/epilogue.
5. Make a tiny vector whose result can be calculated by hand.
6. Compare registers/memory after one iteration, not after the entire loop.
7. If a complex optimized version is failing, use the clear index-based form.
   Correct, bounded code is more valuable than clever code.
8. If the project becomes damaged, make a fresh copy from the unchanged USB
   project and copy only the answer functions into it.

## 16. Final ten-minute gate

### Paper compliance

- Function names and parameter order match exactly.
- Required initialization occurs in the required location.
- Required handler is used only when explicitly demanded.
- Constants, periods, dimensions and pin/button mappings match the paper.
- No prohibited instruction or library call is used.

### Assembly correctness

- R4-R11 preserved.
- LR saved before nested `BL`.
- SP restored on every return path.
- SP aligned to eight bytes at public calls.
- Correct `LDRB/LDRSB/LDRH/LDRSH/LDR` and stores.
- Correct signed or unsigned branches.
- Loop bounds cannot access beyond an array or matrix.
- Flags are not accidentally destroyed when they are outputs.

### C/peripheral correctness

- Interrupt-shared variables are `volatile`.
- Pending flags are acknowledged.
- ISR work is short unless the paper requires otherwise.
- Exactly one owner exists per interrupt vector and timer resource.
- Timer calculation and reset behavior match the requirement.
- ADC/DAC ranges and lookup-table wrap are safe.
- Repeated attempts reset only the state that should reset.

### Build and submission

1. Rebuild the `ARM Exam` target.
2. Require `0 Error(s), 0 Warning(s)`.
3. Confirm the project opens from the copied directory, not from a path on the
   preparation machine.
4. Confirm the final answer files are saved.
5. Submit only `ARM_Exam_Project`.
6. Confirm `Study Material` is not inside the submitted folder or archive.

## 17. Fast link panel

- [Markdown library map](README.md)
- [Code-template index](../Exam%20Atlas%20and%20Code%20Patterns/CODE_TEMPLATES/00_TEMPLATE_INDEX.md)
- [Quick wording lookup](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/QUICK_PATTERN_LOOKUP.md)
- [Code-first pattern index](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/CODE_PATTERN_INDEX.md)
- [All exams](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/exams/INDEX.md)
- [Pattern library](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/INDEX.md)
- [Bulls and Cows practice lab](../Practice%20Projects/BULLS_AND_COWS_DEBUG_LAB/DEBUG_AND_LEARN.md)
- [Current completeness audit](../Tests%20and%20Reports/FINAL_PROJECT_TEMPLATE_AND_EXAM_AUDIT.md)

The current history does not require CAN, MIDI/music, LCD/GLCD, touch-panel or
PCON code. Do not add unrelated modules during the exam.

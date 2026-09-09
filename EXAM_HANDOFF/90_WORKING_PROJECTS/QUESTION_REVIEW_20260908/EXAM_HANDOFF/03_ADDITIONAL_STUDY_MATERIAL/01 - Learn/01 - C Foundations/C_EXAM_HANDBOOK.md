# C exam handbook

This is the C counterpart to the assembly handbook. It is organized around
what you must recognize, write, test, and debug during an LPC1768 exam. The
current project lists `Source/sample.c` and `Source/ASM_funct.s` as answer files.
For object storage, arrays, matrices, structures, `volatile`, ARMASM directives,
and shared C/assembly data, use [Defining data](defining-data.md).

## 1. The sole official starting project

Use only `01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API` as the
starting project. Copy that complete directory, open `sample.uvprojx`, and edit
`Source/sample.c` plus `Source/ASM_funct.s` when the paper requires assembly.

The public contract is `Source/exam_api/exam_api.h`. The project-level
`EXAM_API_QUICK_REFERENCE.md` explains the same declarations. Do not copy API
names from older handbooks, generated recipes, or retired two-file projects.

Call `exam_init()` once. Initialize only the hardware required by the question.
Use `__WFI()` from `LPC17xx.h` when the foreground has no immediate work.

## 2. Why headers exist, and why you do not edit one here

A header normally shares declarations between multiple C translation units.
For example:

```c
/* maths.h: declaration only */
uint32_t clamp(uint32_t value, uint32_t maximum);
```

```c
/* maths.c: one definition */
#include "maths.h"
uint32_t clamp(uint32_t value, uint32_t maximum)
{
  return value < maximum ? value : maximum;
}
```

```c
/* application.c: sees the same declaration */
#include "maths.h"
uint32_t result = clamp(input, 100u);
```

The header prevents every caller from inventing a possibly different type. It
does not normally allocate storage or contain ordinary function bodies.

The clean exam project has one editable C file, so a student-managed header is
usually unnecessary. Declare answer functions near the top of `main.c`.

```c
/* Declaration: no body, no storage for code. */
static uint32_t next_value(uint32_t current);

/* Assembly declaration: definition is exported by assembly.s. */
uint32_t asm_answer(const uint32_t *values, uint32_t count);

/* Definition: the body exists exactly once. */
static uint32_t next_value(uint32_t current)
{
  return current * 3u + 1u;
}
```

Use `static` for a C helper needed only by `main.c`. Do not use `static`
for a C function that assembly imports, because a static symbol is file-local.

## 3. A complete C answer skeleton

```c
#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
  exam_init();

  /* Initialize only what the paper requires. */

  for (;;) {
    /* Consume events or perform bounded foreground work here. */
    __WFI();
  }
}
```

Add handlers only when the paper requires them. A handler must acknowledge its
source, publish the minimum state needed by foreground code, and return quickly.
Never create a second handler with the same vector name.

## 4. Types: choose width and signedness deliberately

Prefer fixed-width types when hardware layout or assembly contracts matter:

| Type | Use |
|---|---|
| `uint8_t` | LED masks, bytes, packed fields |
| `int8_t` | Signed byte data |
| `uint16_t` | ADC/DAC values, halfwords |
| `int16_t` | Signed samples |
| `uint32_t` | Registers, counters, masks, addresses, ordinary ARM values |
| `int32_t` | Signed arithmetic and signed comparisons |
| `uint64_t` | Products, accumulated timing, wide results |
| `bool` | Logical state when no bit mask is needed |

Unsigned wrap is defined modulo `2^N`; signed overflow is not a safe portable
technique. Use `uint32_t` for timer-difference arithmetic:

```c
uint32_t elapsed = end_count - start_count;
```

For overflow-safe scaling:

```c
uint32_t percent = ((uint32_t)sample * 100u + 2047u) / 4095u;
```

Promote before multiplying when the intermediate may exceed the narrow type:

```c
uint64_t product = (uint64_t)a * (uint64_t)b;
```

## 5. Functions

### Define before use

```c
static uint32_t square(uint32_t value)
{
  return value * value;
}

static uint32_t sum_of_squares(uint32_t a, uint32_t b)
{
  return square(a) + square(b);
}
```

### Or declare first and define later

```c
static uint32_t square(uint32_t value);

static uint32_t sum_of_squares(uint32_t a, uint32_t b)
{
  return square(a) + square(b);
}

static uint32_t square(uint32_t value)
{
  return value * value;
}
```

### Return multiple values through pointers

```c
static exam_status_t min_max(const uint32_t *values, uint32_t count,
                             uint32_t *minimum, uint32_t *maximum)
{
  uint32_t i;
  uint32_t lo;
  uint32_t hi;

  if (values == 0 || minimum == 0 || maximum == 0 || count == 0u)
    return EXAM_BAD_ARGUMENT;

  lo = values[0];
  hi = values[0];
  for (i = 1u; i < count; ++i) {
    if (values[i] < lo) lo = values[i];
    if (values[i] > hi) hi = values[i];
  }
  *minimum = lo;
  *maximum = hi;
  return EXAM_OK;
}
```

## 6. Pointers, arrays, and bounds

For a real array in its defining scope, get the element count with:

```c
uint32_t values[] = {4u, 7u, 9u, 2u};
uint32_t count = sizeof values / sizeof values[0]; /* 4 elements */
```

`sizeof values` alone is the size in bytes. The division converts bytes to
elements. This works only while `values` is an actual array.

An array argument becomes a pointer and carries no length. Inside a function,
`sizeof(values) / sizeof(values[0])` therefore gives the wrong result. Compute
the count at the caller and pass it separately:

```c
static uint32_t sum_words(const uint32_t *values, uint32_t count)
{
  uint32_t sum = 0u;
  uint32_t i;
  for (i = 0u; i < count; ++i) sum += values[i];
  return sum;
}
```

Call it from the scope that still knows the array:

```c
uint32_t total = sum_words(values, count);
```

Check before reading element zero. This is wrong for `count == 0`:

```c
uint32_t maximum = values[0];
```

Use `const` when a function must not modify input. Use a pointer only after
validating it when null is possible.

### Row-major matrices

For `rows × columns`, element `(row,column)` is:

```text
index = row * columns + column
```

```c
static uint32_t matrix_get(const uint32_t *matrix, uint32_t columns,
                           uint32_t row, uint32_t column)
{
  return matrix[row * columns + column];
}
```

Nested traversal:

```c
for (row = 0u; row < rows; ++row) {
  for (column = 0u; column < columns; ++column) {
    sum += matrix[row * columns + column];
  }
}
```

## 7. Loops and early exits

Counted loop:

```c
for (i = 0u; i < count; ++i) { /* exactly count iterations */ }
```

Reverse loop without unsigned underflow:

```c
for (i = count; i != 0u; --i) {
  use(values[i - 1u]);
}
```

Search with early return:

```c
static int32_t find_value(const uint32_t *a, uint32_t n, uint32_t wanted)
{
  uint32_t i;
  for (i = 0u; i < n; ++i)
    if (a[i] == wanted) return (int32_t)i;
  return -1;
}
```

Nested search with duplicate consumption needs a `used[]` array or frequency
table; a naive all-pairs count normally overcounts duplicates.

## 8. Structures, enums, and state machines

Use an enum so legal states are explicit:

```c
typedef enum {
  GAME_WAIT_START = 0,
  GAME_EDIT,
  GAME_SHOW_RESULT,
  GAME_FINISHED
} game_state_t;
```

Use one switch for transitions:

```c
static void handle_select(void)
{
  switch (state) {
    case GAME_WAIT_START: capture_secret(); begin_guess(); break;
    case GAME_EDIT:       evaluate_guess(); break;
    case GAME_SHOW_RESULT:begin_guess(); break;
    case GAME_FINISHED:   break;
    default:              state = GAME_WAIT_START; break;
  }
}
```

Write the transition table on paper first: current state, event, action, next
state. Generate a secret only on the transition required by the question.

## 9. Bits and registers

Set bits:

```c
reg |= mask;
```

Clear bits:

```c
reg &= ~mask;
```

Replace a field safely:

```c
reg = (reg & ~FIELD_MASK) | ((value << FIELD_SHIFT) & FIELD_MASK);
```

Test any bit:

```c
if ((flags & mask) != 0u) { }
```

Do not write `if (flags == mask)` when several event bits may be set together.
For write-one-to-clear interrupt registers, write the captured flag mask; do
not use a read-modify-write unless the device documentation requires it.

## 10. Volatile, interrupts, and atomicity

`volatile` tells the compiler that a value may change outside normal code
flow. It does not make a multi-step operation atomic.

```c
static volatile uint32_t pending_events;
```

Safe extraction:

```c
static uint32_t take_events(void)
{
  uint32_t saved = exam_critical_enter();
  uint32_t result = pending_events;
  pending_events = 0u;
  exam_critical_exit(saved);
  return result;
}
```

Keep callbacks and ISRs short: capture, acknowledge, set an event, return.
Long algorithms and state transitions belong in the foreground loop in `main`.

## 11. Function pointers and callbacks

Function pointers are still important C, but the Official Combined Exam API
does not register application callbacks. Use the exact interrupt handler named
by the startup file or the exam, then transfer work to foreground code with
`exam_events_set()` and `exam_events_take()` when appropriate.

If a professor-supplied interface accepts a callback, pass the function name
without parentheses and match its declared signature exactly. Do not invent a
callback API around the Combined template.

## 12. Timers

The Combined API configures MR0 with the timer's actual peripheral clock and
`PR = 0`. Configuration stops and resets the timer; start it explicitly.

```c
exam_status_t status;
status = exam_timer_config_ms(EXAM_TIMER0, 100u, EXAM_TIMER_PERIODIC);
if (status == EXAM_OK) {
  exam_timer_start(EXAM_TIMER0);
}
```

In `TIMER0_IRQHandler`, call `exam_timer_ack(EXAM_TIMER0)` once and test the
returned pending bits. Use `exam_timer_read()` for a snapshot. Use direct
registers for capture, MR1-MR3, custom prescalers, counter input, or MAT output.

## 13. Buttons and joystick

Call `exam_buttons_init()` for the three active-low buttons. A raw EINT handler
acknowledges with `exam_button_ack()`. For debouncing, configure the sample and
confirmation periods, begin debounce from the EINT handler, and call
`exam_debounce_tick()` from one periodic time source.

Joystick input is polling-based:

```c
uint32_t previous = 0u;
exam_joystick_init();
for (;;) {
  uint32_t current = exam_joystick_read();
  uint32_t pressed = exam_joystick_pressed_edges(previous, current);
  previous = current;
  if ((pressed & EXAM_JOY_UP) != 0u) {
    exam_led_toggle(11u);
  }
}
```

## 14. ADC

The Combined API owns potentiometer ADC channel 5 one conversion at a time.

```c
uint16_t raw;
exam_adc_init();
exam_adc_start();
if (exam_adc_take(&raw) != 0u) {
  exam_led_write((uint8_t)(raw >> 4));
  exam_adc_start();
}
```

Call `exam_adc_irq_capture()` from `ADC_IRQHandler` when using the ADC interrupt.
A returned zero from `exam_adc_take()` means no fresh completed sample is ready.

## 15. DAC

Initialize the DAC and write validated 10-bit samples directly:

```c
exam_dac_init();
if (exam_dac_write(sample_10_bit) != EXAM_OK) {
  /* Handle a sample outside 0..1023. */
}
```

The API does not provide waveform playback. When a question needs sound, use a
timer handler or another required time source to advance a bounded sample table
and call `exam_dac_write()` for each value.

## 16. Direct interrupt handlers

Use callback mode unless the paper requires the vector. In direct mode, only
one linked object may own the exact symbol.

```c
void TIMER0_IRQHandler(void)
{
  uint32_t flags = LPC_TIM0->IR;
  LPC_TIM0->IR = flags;
  exam_events_set(EVENT_TIMER);
}
```

Required chain:

```text
power -> clock -> pins -> peripheral source -> clear stale flag
-> clear NVIC pending -> enable NVIC -> enable peripheral
```

Repeated immediate entry usually means the source flag was not acknowledged.
A handler never entered usually means wrong symbol, source/NVIC disabled, or
global interrupts disabled.

## 17. C calls assembly

Near the top of `main.c`:

```c
uint32_t BullsAndCows(int guess[4], int secret[4],
                      int guess_frequency[4], int secret_frequency[4]);
```

Call normally:

```c
result = BullsAndCows(guess, secret, gf, sf);
```

In `assembly.s`:

```asm
                EXPORT  BullsAndCows
BullsAndCows    PROC
                ; R0-R3 contain the four pointers; return integer in R0.
                BX      LR
                ENDP
```

The C prototype determines the register interpretation. A wrong type may
compile yet pass the wrong width, signedness, or pointer/value shape.

## 18. Assembly calls C

In `main.c`:

```c
uint32_t c_policy(uint32_t value, uint32_t limit)
{
  return value < limit ? value : limit;
}
```

In assembly:

```asm
                IMPORT  c_policy
asm_wrapper     PROC
                PUSH    {R4,LR}
                BL      c_policy
                POP     {R4,PC}
                ENDP
```

Do not mark `c_policy` static. The assembly caller must save LR before `BL`.

## 19. Common exam algorithms in C

Frequency table:

```c
for (i = 0u; i < alphabet; ++i) frequency[i] = 0u;
for (i = 0u; i < count; ++i) ++frequency[values[i]];
```

Insertion sort:

```c
for (i = 1u; i < count; ++i) {
  uint32_t key = a[i];
  j = i;
  while (j != 0u && a[j - 1u] > key) {
    a[j] = a[j - 1u];
    --j;
  }
  a[j] = key;
}
```

Recurrence with previous state:

```c
out[0] = seed;
for (i = 1u; i < count; ++i) out[i] = recurrence(out[i - 1u], i);
```

Separate the policy function so an exam correction changes one localized
formula rather than the traversal.

## 20. Testing checklist

For an algorithm, test:

- Empty input if allowed.
- One element.
- Minimum and maximum configured length.
- All equal.
- Already sorted and reverse sorted.
- Signed extremes when signed.
- Duplicates and sentinels.
- Guard values before and after output arrays.

For a state machine, test:

- Initial state.
- Every legal transition.
- Events in the wrong state.
- Repeated event.
- Simultaneous events.
- Delayed foreground processing.
- Stop/restart.
- Resource conflict and initialization failure.

For callbacks, set a breakpoint in the callback and another where the event is
consumed. Confirm the callback is short and the foreground performs the work.

## 21. Error map

| Symptom | Likely cause |
|---|---|
| Undefined symbol | Missing definition, missing `EXPORT`, spelling mismatch, or stale assembly object |
| Multiple definition | Two `main`s, two vector owners, or body placed in included header |
| Incompatible function pointer | Callback signature does not exactly match API typedef |
| HardFault on function return | Bad pointer, corrupted SP/LR, wrong assembly prototype |
| Timer callback never runs | Failed start, ownership conflict, disabled source/NVIC, wrong timer |
| Interrupt repeats forever | Peripheral flag not acknowledged correctly |
| Events disappear | Non-atomic read/clear or missing `volatile` |
| Array corruption | Wrong bound, width, stride, or output capacity |
| ADC always old/zero | DONE not checked, wrong channel, trigger not started |
| DAC pitch wrong | Confused waveform frequency with sample/update frequency |

## 22. Final C exam checklist

```text
1. Write inputs, outputs, states, events, timing, and ownership on paper.
2. Choose exact-width types and signedness.
3. Add declarations near the top of main.c.
4. Keep private helpers static.
5. Initialize only required devices in the initialization section of `main`.
6. Check every status return.
7. Keep callbacks short and signatures exact.
8. Consume volatile event state atomically in the foreground loop in `main`.
9. Use masks for combined inputs and interrupt flags.
10. Validate pointers, counts, ranges, and capacities before access.
11. Rebuild All after changing assembly.
12. Test nominal, boundary, duplicate, and failure scenarios.
```

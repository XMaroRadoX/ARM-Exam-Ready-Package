# C course for the ARM exam

This is the guided C route for the programming part of the exam. Complete the
core route in order, then use the final lookup table when a question asks for a
specific operation. Every board example uses `Source/sample.c` in the sole
`Official Combined Exam API` project and its public `exam_api.h` interface.

The exam normally couples a C board program to an assembly routine. C must
initialize the board, collect inputs, own timers and interrupts, maintain the
state machine, call assembly with the exact prototype, and display or stream the
result. The assembly algorithm is covered separately.

## Core route

1. Program shape, declarations and types.
2. Functions, pointers, arrays and matrices.
3. Bits, arithmetic and result encoding.
4. Structures, enums and state machines.
5. Interrupt-safe events and handlers.
6. LEDs, buttons, joystick, timers, ADC and DAC.
7. Calling assembly and debugging the complete project.

Use the [C exam handbook](C_EXAM_HANDBOOK.md) as the deeper language reference,
[Defining data](defining-data.md) for storage/linkage/layout, and the
[Official Combined Exam API quick reference](../../../01_EXAM_READY/02_STARTING_TEMPLATES/Official%20Combined%20Exam%20API/EXAM_API_QUICK_REFERENCE.md)
for every supported helper.

## Lesson 1: build the smallest valid program

Answer C code goes in `Source/sample.c`. Keep the first build tiny:

```c
#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
  exam_init();

  for (;;) {
    __WFI();
  }
}
```

Rules:

- Call `exam_init()` once and first.
- Initialize only the components named by the question.
- Keep repeated foreground work inside the infinite loop.
- Keep the clean original project unchanged; work in a copy.
- Build before editing and after every small working part.

## Lesson 2: declarations, definitions and storage

A declaration tells the compiler a name and type. A definition allocates the
object or supplies the function body.

```c
static uint32_t next_value(uint32_t current); /* declaration */

static uint32_t counter;          /* zero-initialized definition */
static volatile uint32_t events;  /* shared with an interrupt */
static const uint16_t sine[4] = {512u, 800u, 512u, 224u};

static uint32_t next_value(uint32_t current)  /* definition */
{
  return current + 1u;
}
```

Use:

- `static` at file scope for private state and helpers.
- `static volatile` for private state written asynchronously by an ISR.
- `const` for tables that must not change.
- Static storage for large arrays; do not place a 1,000-word array on the
  ordinary local stack.
- One definition for a shared symbol and `extern` declarations elsewhere.

Do not put a normal initialized object definition in a header. Read
[Defining data](defining-data.md) for C/assembly objects, structures, alignment,
padding and linker errors.

## Lesson 3: widths, signedness and operators

Use fixed-width types when C and assembly share a contract:

| Need | Type |
|---|---|
| Byte or LED mask | `uint8_t` |
| Signed byte | `int8_t` |
| ADC/DAC sample | `uint16_t` |
| Ordinary ARM word/mask/counter | `uint32_t` |
| Signed word | `int32_t` |
| Wide product or sum | `uint64_t` / `int64_t` |

Important operator pairs:

```c
uint32_t bit = (word >> position) & 1u; /* bitwise AND */
if ((ready != 0u) && (count > 0u)) { }  /* logical AND */
word ^= mask;                            /* XOR */
word |= mask;                            /* set bits */
word &= ~mask;                           /* clear bits */
```

Parenthesize encoded results. Do not rely on remembering precedence under exam
pressure:

```c
uint32_t encoded = (((2u * exact) - 1u) << 4)
                 + ((2u * partial) - 1u);
```

Unsigned arithmetic wraps modulo `2^N`. Signed overflow is not a safe portable
technique. Promote before a wide multiplication:

```c
uint64_t product = (uint64_t)a * (uint64_t)b;
```

## Lesson 4: functions and output parameters

Write the contract before the body:

```c
/* Returns EXAM_OK and writes both outputs when values/count/outputs are valid. */
static exam_status_t min_max(const int32_t *values, uint32_t count,
                              int32_t *minimum, int32_t *maximum)
{
  uint32_t i;
  int32_t lo;
  int32_t hi;

  if ((values == 0) || (minimum == 0) || (maximum == 0) || (count == 0u)) {
    return EXAM_BAD_ARGUMENT;
  }

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

Checklist:

- Validate pointers before dereferencing.
- Validate `count` before reading element zero.
- Use `const` for input that must not be modified.
- State whether partial output is allowed on failure.
- Use a status plus pointer outputs for multiple results.

## Lesson 5: arrays, matrices and bounds

An array parameter does not contain its length. Pass pointer plus count:

```c
static uint32_t sum_words(const uint32_t *values, uint32_t count)
{
  uint32_t i;
  uint32_t sum = 0u;

  for (i = 0u; i < count; ++i) {
    sum += values[i];
  }
  return sum;
}
```

C matrices are row-major. For a flat `rows x columns` matrix:

```c
uint32_t index = row * columns + column;
value = matrix[index];
```

For an output buffer, pass capacity and check before every store:

```c
if (written >= capacity) {
  return EXAM_OUT_OF_RANGE;
}
output[written++] = value;
```

Safe reverse loop for unsigned indexes:

```c
for (i = count; i != 0u; --i) {
  use(values[i - 1u]);
}
```

Do not write `i >= 0u`; that is always true for an unsigned value.

## Lesson 6: bits, packed fields and timer-derived values

Extract a field:

```c
static uint32_t field_get(uint32_t word, uint32_t shift, uint32_t width)
{
  uint32_t mask;

  if ((width == 0u) || (width > 32u) || (shift >= 32u) ||
      (width > (32u - shift))) {
    return 0u;
  }
  mask = (width == 32u) ? UINT32_MAX : ((1u << width) - 1u);
  return (word >> shift) & mask;
}
```

Insert a field while preserving unrelated bits:

```c
static uint32_t field_put(uint32_t word, uint32_t value,
                          uint32_t shift, uint32_t width)
{
  uint32_t low_mask;
  uint32_t field_mask;

  if ((width == 0u) || (width > 32u) || (shift >= 32u) ||
      (width > (32u - shift))) {
    return word;
  }
  low_mask = (width == 32u) ? UINT32_MAX : ((1u << width) - 1u);
  field_mask = low_mask << shift;
  return (word & ~field_mask) | ((value << shift) & field_mask);
}
```

Generate four two-bit digits from a timer snapshot:

```c
for (i = 0u; i < 4u; ++i) {
  secret[i] = (timer_snapshot >> (4u * i)) & 0x3u;
}
```

These versions reject out-of-range fields and handle a full 32-bit field
without shifting by 32, which would be invalid C.

## Lesson 7: safe scaling and overflow order

ADC value to percentage:

```c
uint32_t percent = ((uint32_t)sample * 100u + 2047u) / 4095u;
```

When a question warns that an intermediate product may overflow, divide a
known divisible scale first or use a 64-bit temporary:

```c
uint32_t span = maximum - minimum;
uint32_t scaled = (uint32_t)(((uint64_t)value * span) / value_maximum);
uint32_t threshold = (maximum - scaled) / divisor;
```

Also decide what happens when `value_maximum == 0u`. Never silently divide by
zero.

## Lesson 8: enums and state machines

Model legal states explicitly:

```c
typedef enum {
  STATE_WAIT_START = 0,
  STATE_EDIT_GUESS,
  STATE_SHOW_RESULT,
  STATE_FINISHED
} app_state_t;

static app_state_t state;
```

Keep transitions in one foreground function:

```c
static void handle_select(void)
{
  switch (state) {
    case STATE_WAIT_START:
      start_game();
      state = STATE_EDIT_GUESS;
      break;
    case STATE_EDIT_GUESS:
      evaluate_guess();
      state = won ? STATE_FINISHED : STATE_SHOW_RESULT;
      break;
    case STATE_SHOW_RESULT:
      clear_guess();
      state = STATE_EDIT_GUESS;
      break;
    case STATE_FINISHED:
      break;
    default:
      state = STATE_WAIT_START;
      break;
  }
}
```

Write a state/event table before coding. For each transition list current state,
event, guard, actions, next state, and which data must persist.

## Lesson 9: interrupts, `volatile` and foreground handoff

The Official Combined Exam API does not register application callbacks. Write
the exact handler required by the startup file or paper. Keep the handler short:
acknowledge the source, copy data if required, set an event, and return.

```c
enum { EVENT_BUTTON = 1u << 0 };

void EINT0_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_INT0);
  exam_events_set(EVENT_BUTTON);
}

void foreground_step(void)
{
  if ((exam_events_take(EVENT_BUTTON) & EVENT_BUTTON) != 0u) {
    exam_led_toggle(11u);
  }
}
```

Use `volatile` for state changed asynchronously. For a multi-step shared
snapshot, protect only the copy with `exam_critical_enter()` and
`exam_critical_exit()`; perform slow work after leaving the critical section.

## Lesson 10: board components

### LEDs

Single-LED calls accept board labels `4..11`; display masks retain bit 0 for LD11
and bit 7 for LD4. Use `exam_led_on()`, `exam_led_off()`,
`exam_led_toggle()`, `exam_led_one_hot()`, `exam_led_write()`,
`exam_led_read()`, and `exam_led_clear()` exactly as declared.

### Debounced buttons

Call `exam_buttons_init()`, configure the sample and confirmation periods with
`exam_debounce_config()`, begin a button from its EINT handler with
`exam_debounce_begin()`, and call `exam_debounce_tick()` from one periodic time
source. Consume confirmed presses with `exam_button_events_take()`.

### Joystick

Call `exam_joystick_init()`, poll `exam_joystick_read()`, and calculate new
presses with `exam_joystick_pressed_edges(previous, current)`. The returned
`EXAM_JOY_*` bits are one when pressed.

### Periodic timer

```c
if (exam_timer_config_ms(EXAM_TIMER0, 500u, EXAM_TIMER_PERIODIC) == EXAM_OK) {
  exam_timer_start(EXAM_TIMER0);
}
```

A timer handler calls `exam_timer_ack()` and tests bit 0 for MR0. Use direct
registers for capture, MR1-MR3, custom prescalers, counter input, or MAT output.

### Potentiometer and ADC

```c
uint16_t sample;
exam_adc_init();
exam_adc_start();
if (exam_adc_take(&sample) != 0u) {
  exam_led_write((uint8_t)(sample >> 4));
  exam_adc_start();
}
```

### DAC and speaker

```c
exam_dac_init();
(void)exam_dac_write(sample_10_bit);
```

For waveform playback, advance a bounded sample table from a timer handler and
write each value with `exam_dac_write()`. The Combined API does not hide timer
ownership behind a playback service.

## Lesson 11: C calls assembly

The declaration, call and exported symbol must agree exactly:

```c
/* Near the top of main.c. */
uint32_t solve_maze(uint8_t *matrix, uint32_t rows, uint32_t columns);

uint32_t result = solve_maze(maze, ROWS, COLUMNS);
```

```asm
                EXPORT  solve_maze
solve_maze      PROC
                ; R0 = matrix, R1 = rows, R2 = columns
                ; R0 = returned result
                BX      LR
                ENDP
```

The first four argument words use `R0-R3`; later words are on the caller's
stack. A 64-bit argument/result uses consecutive register words according to
the exact AAPCS contract. Assembly preserves every modified `R4-R11`, preserves
`LR` in a non-leaf function, and restores `SP` exactly.

Use a temporary assembly stub if Q1 is unfinished but Q2 needs to link:

```asm
asm_answer      PROC
                EXPORT  asm_answer
                MOVS    R0, #0
                BX      LR
                ENDP
```

## Lesson 12: exact handlers and direct registers

Use high-level board functions when peripheral setup is not graded. If the
question explicitly grades register programming, use CMSIS registers and own
the vector.

For an exact `TIMER0_IRQHandler`, set `EXAM_OWN_TIMER0_HANDLER` to `1` in
`exam_config.h`. Do not also start the library callback service for Timer0.

```c
void TIMER0_IRQHandler(void)
{
  uint32_t pending = LPC_TIM0->IR;
  LPC_TIM0->IR = pending; /* write-one-to-clear */
  exam_events_set(EVENT_TICK);
}
```

Read pending flags once and clear the same bits. Assign one owner to every
timer, match channel, interrupt vector, RIT/SysTick service, ADC conversion and
DAC stream.

## How do I do a specific exam task?

| Need | Method |
|---|---|
| Define a helper | Prototype near top, `static` body in `main.c` |
| Return two values | Status return plus validated output pointers |
| Pass an array | Pointer plus count; `const` for read-only input |
| Pass a matrix | Flat pointer plus dimensions; row-major index |
| Allocate a large array | File-scope `static`, not an ordinary local |
| Share with an ISR | Short callback plus event flags; `volatile` only when direct sharing is necessary |
| Debounce input | Start RIT scheduler, set confirmation period, initialize buttons/joystick |
| Use the first joystick movement | `joystick_first_movement()` and reset it at the new round |
| Generate a random-looking seed | Read a free-running timer snapshot and mask/extract fields |
| Blink periodically | Periodic timer callback sets an event; foreground changes the state/output |
| Stop after one duration | Match with interrupt + reset + stop, or stop explicitly in the callback |
| Read the potentiometer | Call `exam_adc_init()` once, start a conversion with `exam_adc_start()`, and consume a fresh result with `exam_adc_take()` |
| Play samples | DAC table plus owned timer; stop playback before timer reuse |
| Call assembly | Exact prototype in C, exact `EXPORT` in assembly |
| Use five or more arguments | First four words in registers, remaining words on caller stack |
| Avoid overflow | Promote to 64 bits or change evaluation order as the contract permits |
| Handle duplicate matches | Frequency arrays or consume-once marker arrays |
| Preserve a secret across rounds | Static game state; reset guess only, not secret |
| Diagnose an undefined symbol | Compare spelling/case/prototype/`EXPORT`/project inclusion |
| Diagnose a hard fault after return | Check LR, callee-saved registers, PUSH/POP, SP alignment and bounds |

## Algorithm course map

For an algorithm question, first write a clear C version with the exact widths,
mutation rule, capacity and invalid-input behavior. Use that version as the
oracle for the assembly routine.

| Question shape | Start with |
|---|---|
| Find an item or insertion point | linear search; binary search/lower bound |
| Reorder an array | reversal/rotation; insertion, selection, bubble, merge, quick, heap or bounded counting sort |
| Reduce values | signed/unsigned min, max, sum; histogram/mode; prefix or range sum |
| Work with decimal digits | extraction/reconstruction; palindrome; digit sum; Kaprekar step |
| Work with packed bits | population count/parity; bitfield get/put; packed transpose/matrix multiplication |
| Produce variable-length output | pass output capacity; check before every RLE, look-and-say, string or filter store |
| Match duplicates once | frequency tables or consume-once marker arrays |
| Traverse a graph/maze | explicit-stack DFS, recursive bounded DFS, BFS, flood fill, Dijkstra or union-find |
| Optimize/count choices | bounded knapsack, coin change, LIS or edit distance |
| Process a stream | moving window, checksum/CRC structure, ring buffer, circular queue or stack |
| Generate a recurrence | identify all earlier indexes, guard bounds, then LCG/Recaman/Hofstadter-style update |
| Avoid expensive multiplication/division | Horner form, exponentiation by squaring, Euclid GCD, integer square root or restoring division |

The [maximum algorithm reference](../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/README.md)
contains the complete C and ARM pair for each method, including contracts,
complexity, edge cases and vectors. Use its **High priority** section first;
the supplementary section is a lookup library, not a list to memorize.

## Practice sequence

1. Type the minimal `main.c` from memory and build it.
2. Add one button event and one LED response.
3. Add a periodic timer without doing long work in its callback.
4. Add a free-running timer seed and display its low byte.
5. Read the potentiometer and display the high eight bits.
6. Call the identity `asm_solution`, then replace it with a small real routine.
7. Build a three-state joystick game.
8. Solve one paper using the [past-exam workstation](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/exams/index.html).

Before the exam, complete at least one ADC paper, one DAC paper, one multi-timer
paper, one joystick state-machine paper, one stacked-argument assembly paper and
one exception/startup paper.

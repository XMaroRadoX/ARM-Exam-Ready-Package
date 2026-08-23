# Live ARM exam companion

Use this document after the paper is in front of you. Work from the current
checkpoint only. Do not jump into code before the contract checkpoint is done.

## Checkpoint 1 — You have just received the paper

Do these four things now:

1. Copy `ARM_Exam_Project` from the USB drive to a writable exam folder.
2. Leave the USB copy untouched as recovery.
3. Open `ARM_Exam_Template.uvprojx`.
4. Build target `ARM Exam` before changing a file.

Expected baseline:

```text
0 Error(s), 0 Warning(s)
```

If the baseline fails, stop. This is an environment/copy problem, not your
algorithm. Confirm the whole folder was copied and Compiler 6 is selected.

In the Keil Project pane you should see one expanded group:

```text
ARM Exam
└── EDIT HERE - C AND ASM FIRST
    ├── exam_user.c
    ├── exam_asm.s
    └── exam_user.h
```

The support files below those three are already linked.

## Checkpoint 2 — Split the paper into Q1 and Q2

On paper, fill this in with the exact wording:

```text
Q1 symbol:
Q1 R0:
Q1 R1:
Q1 R2:
Q1 R3:
Q1 stack arguments:
Q1 return value/registers:
Q1 element width:
Q1 signed or unsigned:
Q1 modifies input memory:
Q1 helper call required:
Q1 flags returned:

Q2 input events:
Q2 output:
Q2 timers and periods:
Q2 ADC/DAC:
Q2 exact handler required:
Q2 work required inside handler:
```

Do not continue until every known item is filled. Write “not specified” instead
of inventing an answer.

## Checkpoint 3 — Identify Q1’s shape

Choose the matching branch.

### Branch A — Array or sequence

Clues: “array,” “N elements,” “series,” “subsequent value,” “until,” or “store
the result.”

Open:

- `CODE_TEMPLATES/02_algorithms/array_scan_word.s` for word arrays.
- `CODE_TEMPLATES/02_algorithms/recurrence_into_array.s` for sequences.
- `CODE_TEMPLATES/02_algorithms/fixed_point_recurrence.s` for Q-format math.

Decide now:

```text
byte -> LDRB/STRB
signed byte -> LDRSB/STRB
halfword -> LDRH/STRH
signed halfword -> LDRSH/STRH
word -> LDR/STR, index scaled by 4
```

### Branch B — Matrix, maze, graph, neighbors

Clues: “rows,” “columns,” “neighbor,” “maze,” “right/bottom/left/top,” “DFS,”
“shortest path,” or “Kruskal.”

Start with this formula:

```text
index = row * number_of_columns + column
```

Never use `row * number_of_rows + column` unless the matrix is explicitly
stored with that unusual stride.

Open:

- `CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s`
- `CODE_TEMPLATES/02_algorithms/nested_search_with_break.s`
- Atlas pattern `PAT-ALG-GRAPH-SEARCH-001`

Write the neighbor offsets before writing code:

```text
right  = index + 1
bottom = index + columns
left   = index - 1
top    = index - columns
```

Confirm whether borders prevent underflow/overflow. If only inner cells are
processed, use row `1..rows-2` and column `1..columns-2`.

### Branch C — Sorting, minimum/maximum, digit reorder

Clues: “ascending,” “descending,” “sort,” “minimum,” “maximum,” or “reorder
digits.”

Use the 2023-02-07 insertion-sort answer as the complete historical example.
Use the array and nested-loop templates for structure. Do not trust the current
2023-02-24 placeholder as a complete Kaprekar solution.

Decide before coding:

```text
ascending or descending:
signed or unsigned comparison:
in-place or copied output:
byte or word elements:
stable ordering required:
```

### Branch D — Frequency comparison, Bulls and Cows, Mastermind

Clues: “exact,” “partial,” “same value,” “frequency,” “duplicates,” or “matched
position.”

Choose one method:

- Histogram when the value alphabet is small and bounded.
- Marked/matched elements when duplicates must be consumed exactly once.
- Nested search only when size is small and the duplicate rule is explicit.

Use the 2026 Bulls and Cows/Mastermind sources as exam-specific examples.
Test repeated values; nominal all-distinct data is not enough.

### Branch E — SVC, flags, Reset_Handler, exception frame

Clues: “supervisor call,” “SVC immediate,” “PSR/APSR,” “N/Z/C/V,” “stacked
PC,” “MSP/PSP,” or “Reset_Handler.”

Open `CODE_TEMPLATES/04_rare_dangerous` and use only the matching file.

If writing an exact handler, set its `EXAM_OWN_*_HANDLER` switch to 1 before
defining the symbol. Only one linked source may own a vector.

## Checkpoint 4 — Build the assembly frame first

Ask: does Q1 execute `BL`?

### No `BL`

Use a leaf function. If only R0–R3 and R12 are used, no stack frame is needed.

```asm
                EXPORT  required_name
required_name   PROC
                ; algorithm
                BX      LR
                ENDP
```

### Yes, it calls another function

Use a non-leaf frame before writing the algorithm:

```asm
                EXPORT  required_name
required_name   PROC
                PUSH    {R4-R6, LR}
                ; copy any R0-R3 values needed after BL into R4-R6
                BL      helper
                ; finish calculation
                POP     {R4-R6, PC}
                ENDP
```

The push contains four registers, so SP remains eight-byte aligned. Save LR
before the first `BL`.

### Five or more parameters

Capture caller SP before changing it:

```asm
                MOV     R12, SP
                PUSH    {R4-R8, LR}
                LDR     R4, [R12]       ; argument 5
                LDR     R5, [R12, #4]   ; argument 6
                LDR     R6, [R12, #8]   ; argument 7
```

At every return path, restore exactly the same frame.

## Checkpoint 5 — Write one loop and build

Do not write the entire routine before the first build. Add:

1. Symbol and prologue.
2. Input validation/base case.
3. One loop structure.
4. Epilogue.

Build now. Fix syntax and symbol errors before adding the algorithm body.

Safe counted-loop shape:

```asm
                MOVS    R2, #0
loop_check      CMP     R2, R1
                BHS     loop_done
                ; use element R2
                ADDS    R2, R2, #1
                B       loop_check
loop_done
```

If accessing `i+1`, the loop cannot run through `i == length-1`.

## Checkpoint 6 — Connect assembly to C

In `exam_user.c`, write a prototype matching the exact register contract:

```c
extern uint32_t required_name(uint32_t *data, uint32_t length);
```

Check all four:

- C spelling equals assembly spelling, including case.
- Assembly has `EXPORT required_name`.
- Pointer type matches byte/word width.
- Signed C type matches signed assembly loads and comparisons.

Build again. An undefined-symbol error is a name/export/project-inclusion
problem, not an algorithm problem.

## Checkpoint 7 — Classify Q2

Choose the minimum set of peripherals actually named by the paper.

### Buttons or INT0/KEY1/KEY2

```c
(void)exam_buttons_start(exam_button_event);
```

In the callback, capture the confirmed press and set an event. Do longer work
in `exam_user_loop` unless the paper explicitly requires it in the handler.

### Joystick

```c
(void)exam_joystick_start(exam_joystick_event);
```

Directions are masks. Use `current & EXAM_JOY_LEFT`, not equality.

### Periodic timer

```c
(void)exam_timer_every_ms(0, required_ms, exam_timer_event);
```

### Free-running timer without interrupts

```c
(void)exam_timer_prescaler(0u, 0u);
(void)exam_timer_reset(0u);
(void)exam_timer_start(0u);

/* On the required event: */
seed = exam_timer_count(0u);
```

Do not use `exam_timer_every_ms` when the paper says no interrupt and no
reset-on-match.

### ADC/potentiometer

```c
(void)exam_pot_start();
if (exam_pot_read(&sample) == EXAM_OK) {
    /* apply exact paper formula */
}
```

Raw range is 0..4095.

### DAC

```c
(void)exam_dac_write(sample);
```

DAC range is 0..1023. Clamp or validate table data and wrap the table index.

## Checkpoint 8 — Write Q2 as a state machine

List states before coding:

```text
WAIT_INPUT
RUN_REQUESTED
RUNNING
SHOW_RESULT
FINISHED
```

Not every exam needs all of them. Use only the needed states.

Shared callback/main variables are `volatile`:

```c
static volatile uint32_t pending_action;
static volatile exam_button_t last_button;
```

Canonical handoff:

```c
void exam_button_event(exam_button_t button, exam_button_event_t event)
{
    if (event == EXAM_PRESS) {
        last_button = button;
        exam_events_set(EXAM_EVENT_BUTTON);
    }
}

void exam_user_loop(void)
{
    uint32_t events = exam_events_take(EXAM_EVENT_BUTTON);
    if ((events & EXAM_EVENT_BUTTON) != 0u) {
        exam_button_t button = last_button;
        /* state transition or algorithm call */
        (void)button;
    }
}
```

## Checkpoint 9 — Run paper examples

Before testing random values, reproduce the paper’s first complete example.

For Q1, inspect:

- R0 return value.
- Output array/matrix.
- Registers R4–R11 after return.
- SP before and after the call.
- Required flags.

Then test:

1. Minimum legal input.
2. Maximum configured length.
3. Repeated/duplicate values.
4. Already finished or already sorted input.
5. One-iteration boundary.
6. Negative values if signed.

For Q2, exercise:

- Press and release.
- Repeated press.
- Two buttons in both orders.
- Timer before and after a button.
- Stop and restart.
- Last table element wrapping to zero.
- ADC minimum, midpoint, maximum.

## Checkpoint 10 — Something failed

Use the symptom, not guesswork.

### Undefined symbol

Check spelling, `EXPORT`, prototype, and that `exam_asm.s` is in the project.

### Multiply defined handler

You added a handler already owned by the platform. Set the matching
`EXAM_OWN_*_HANDLER` switch or remove your duplicate.

### Works once, fails on second call

Check R4–R11 preservation, LR save, and exact SP restoration.

### Wrong row or diagonal

Check row-major stride and neighbor offsets. Stride is columns.

### One byte/word beyond the array changed

Check `< length` versus `<= length`, `i+1`, and word scaling by four.

### Interrupt never stops

Read and clear the actual pending flags. Hardware flags are commonly
write-one-to-clear.

### Timer period is wrong

Recalculate peripheral clock, divider, prescaler and match value. Confirm
whether the register stores `period` or `period-1` for that peripheral.

## Checkpoint 11 — Final ten minutes

Read this list literally:

- Function symbol matches the paper.
- Parameter order matches the paper.
- Correct byte/halfword/word loads and stores.
- Correct signed or unsigned branches.
- R4–R11 preserved.
- LR saved before `BL`.
- SP eight-byte aligned at calls and restored at returns.
- No out-of-bounds neighbor or `i+1` access.
- Callback/main shared variables are `volatile`.
- Pending interrupt flags are cleared.
- One owner per interrupt vector.
- Timer number and period match the paper.
- ADC/DAC ranges are safe.
- Paper example produces the exact result.
- Rebuild shows zero errors and zero warnings.

## Checkpoint 12 — Submit

Save all files. Rebuild one last time. Submit only the copied
`ARM_Exam_Project` folder.

Before uploading or handing it in, search the submitted folder name. It must
not contain `Study Material`. Your private guide, atlas, historical
answers and tests stay on the USB and are never part of the submission.

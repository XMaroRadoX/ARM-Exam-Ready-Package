# Using the solved answers with the Official Combined Exam API

There is one starting template:

`01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/sample.uvprojx`

Use a copy of that project for an exam attempt. Do not combine it with an older
template, callback layer, compatibility wrapper, or a second peripheral library.

## Where the maintained answers live

The editable source of truth for each full exam is:

`03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/<exam>/Answer Source/`

Each folder contains the maintained `main.c` and `assembly.s`. The files under
`03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/exam-solutions/` are generated
question-by-question copies. Rebuilding the portal refreshes those copies from
the maintained Answer Source folders.

## Start a clean working copy

1. Copy the entire `Official Combined Exam API` folder.
2. Build `sample.uvprojx` before changing any answer code.
3. Copy the complete maintained `main.c` into `Source/sample.c`, including its handlers, `static` state, and helper functions.
4. Put the required assembly routines in `Source/ASM_funct.s`.
5. Keep every public assembly symbol exactly equal to the C `extern` name.
6. Initialize each used peripheral explicitly after `exam_init()`.

## Interrupt ownership

The project already contains one source file for each supported interrupt
family. An exam answer must leave exactly one definition of every vector.

| Answer handler | Template source to edit | Required acknowledgement |
|---|---|---|
| `EINT0_IRQHandler`, `EINT1_IRQHandler`, `EINT2_IRQHandler` | `Source/button_EXINT/IRQ_button.c` | `exam_button_ack(...)` |
| `TIMER0_IRQHandler` through `TIMER3_IRQHandler` | `Source/timer/IRQ_timer.c` | `exam_timer_ack(...)` |
| `SysTick_Handler` | `Source/systick/IRQ_systick.c` | follow the paper; SysTick clears on exception entry |
| `RIT_IRQHandler` | `Source/RIT/IRQ_RIT.c` | `exam_rit_ack()` |
| `ADC_IRQHandler` | `Source/adc/IRQ_adc.c` | `exam_adc_irq_capture()` |

For maintained solved answers, keep the complete answer together in `sample.c`.
In the template files listed above, remove only definitions of handlers already
provided by that answer. Keep handlers it does not provide. For example, the
February 2026 ARM1 answer supplies EINT0, ADC, and RIT handlers: remove EINT0
from `IRQ_button.c`, ADC from `IRQ_adc.c`, and RIT from `IRQ_RIT.c`; leave EINT1,
EINT2, timers, and SysTick in place. Empty IRQ source files may remain in the project.

Do not move an individual handler away from its `static` variables or helper
functions. Those names are local to their C file. If you deliberately split the
answer into modules, design a shared header and explicit state ownership first;
adding `extern` cannot expose another file's `static` variable.

Standalone API teaching snippets show the IRQ source location for a new project.
That convention does not require splitting an existing complete solved answer.
Never leave duplicate handler definitions in both locations.

The supplied `exam_api` owns helper configuration and acknowledgement. The
question owns its state transition and computation. If a paper explicitly
requires direct registers, follow the paper for that resource and do not also
configure the same resource through `exam_api`.

## Physical LED labels

Single-LED API calls now take the printed board label directly: `exam_led_on(11)`
lights LD11 and `exam_led_on(4)` lights LD4. Older calls used GPIO indexes 0..7;
convert their arguments to `11 - old_index` when migrating to this template.
Values 4..7 have changed meaning. Low-level professor functions still use indexes.
`exam_led_write()` already uses bit 7 for LED4 and bit 0 for LED11; do not reverse
its bit masks. `exam_led_one_hot()` sets the display and returns a status.

## Reset-time test storage

Keep `sample.sct` with the copied project. Both targets use this relative linker
file. It reserves the last 16 bytes of the first SRAM bank for `LCG_TEST_DATA`
in an `UNINIT` region, so the July 2025 reset routines' ten test bytes survive
C startup. Other writable data is initialized normally. If you increase `DIM`
past 16, expand that reserved region and reduce the adjacent normal RAM region
accordingly; the linker rejects a test area that exceeds its reservation.

## February 2026 ADC display policy

The three answers use a 10 ms RIT tick and 50 ms button confirmation, a maintained
recommendation rather than a timing constant prescribed by the papers. IRQs
capture ADC input or debounce events; the foreground computes and displays.
Look-and-say and RLE results remain until the potentiometer's high eight bits
change. Recamán playback owns the display until the sequence finishes, including
when the potentiometer moves. Its final element remains until a subsequent
potentiometer change. A new confirmed KEY2 press starts a new sequence.

## Common initialization pairs

| Work needed | Initialization and start |
|---|---|
| LEDs | `exam_init()` initializes them |
| External buttons | `exam_buttons_init()` |
| Timer | configure, check `EXAM_OK`, then `exam_timer_start(...)` |
| SysTick | `exam_systick_config_ticks(...)` or `exam_systick_config_ms(...)` |
| RIT | configure, check `EXAM_OK`, then `exam_rit_start()` |
| Joystick | `exam_joystick_init()`, then sample it periodically |
| ADC | `exam_adc_init()`, start, capture in IRQ, consume, start again |
| DAC | `exam_dac_init()` before the first `exam_dac_write(...)` |

## Validation

From the package root, run:

```powershell
python 01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/BUILD_STUDENT_PORTAL.py
python 01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/VERIFY_COMBINED_SOLUTIONS.py
python 01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/VERIFY_STUDENT_PORTAL.py
```

The solution verifier checks all 48 question directories, C-to-assembly exports,
the sole 52-call header, obsolete helper names, IRQ acknowledgement, and required
peripheral initialization. The portal verifier checks generated pages, links,
inventories, and representative searches. A Keil build and board run are still
required before claiming hardware execution.

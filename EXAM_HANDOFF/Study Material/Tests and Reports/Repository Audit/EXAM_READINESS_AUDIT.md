# Repository exam-readiness audit

## Verdict

The `ARM_Exam_Project` directory is a clean, useful **single-target mixed C and
assembly starting project** for the LPC1768. It is suitable to copy to the exam
drive and adapt to a new paper.

The repository as a whole is **not a fully correct 23-exam solution suite** and
must not be described that way:

- Seven historical Q1 assembly answers are generic placeholders.
- Six of those seven also have generic Q2 C code.
- The 23 historical folders are answer-source collections, not self-contained
  Keil projects; none contains a `.uvprojx` file.
- One exam-specific solution has the wrong affine-matrix byte order
  (`E2025-01-29-A1`).
- One uses 1,000 elements where the paper requires 10,000
  (`E2026-02-18-A2`), with an unresolved 40,000-byte placement problem.
- Several otherwise relevant C answers define interrupt handlers directly.
  They cannot be dropped into the clean project until the matching
  `EXAM_OWN_*_HANDLER` flags are set in `exam_config.h`.
- Existing logs establish earlier compilation for selected artifacts. They do
  not establish linked ARM execution, ABI preservation, peripheral simulation,
  or physical-board behavior for all 23 exams.

Accordingly, the honest status is:

| Item | Audit result |
|---|---|
| Clean submission skeleton | usable |
| C/assembly entry wiring | correct and documented below |
| Coverage of peripherals used by the 23 papers | covered by the API or direct-register access |
| CAN, MIDI, GLCD/touch, PCON | intentionally omitted because they are absent from the indexed history; GLCD/touch was also explicitly excluded |
| Ethernet | absent from both the 15 professor templates and the 23 papers |
| All 23 answer directories present | yes |
| All 23 answers completed | no |
| All 23 answers independently executed in Keil | no |
| Hardware build evidence | prior logs only; a fresh run was unavailable because `UV4.exe` is not installed/discoverable in the present environment |
| Physical board test | not performed |

The detailed classification is in
[EXAM_BY_EXAM_AUDIT.csv](EXAM_BY_EXAM_AUDIT.csv). Do not revise from a
historical answer without checking that row first.

## What was actually inspected

The audit read and indexed:

- all 24 files in the clean project; 22 are textual source/configuration files;
- all 172 files under `Solved Exams`; 171 are textual;
- all 1,039 files in the revised professor-template extraction;
- all 375 textual files there, including every `.c`, `.h`, `.s`, project file,
  option file, linker listing and log that can be decoded as text;
- all 23 indexed ARM papers, comprising 61 pages, by text extraction and a
  complete rendered-page visual pass.

Binary object files, executables, archives and PDFs were read for hashes and
metadata; they were not treated as source code. Repeated CMSIS and course-driver
files are listed at every path even when their hashes are identical.

Machine-readable inventories:

- [AUDIT_SCOPE_SUMMARY.csv](AUDIT_SCOPE_SUMMARY.csv)
- [CURRENT_PROJECT_FILES.csv](CURRENT_PROJECT_FILES.csv)
- [SOLVED_EXAM_FILES.csv](SOLVED_EXAM_FILES.csv)
- [PROFESSOR_TEMPLATE_FILES.csv](PROFESSOR_TEMPLATE_FILES.csv)
- [EXAM_SOURCE_PDF_MAP.csv](EXAM_SOURCE_PDF_MAP.csv)
- [PROFESSOR_TEMPLATE_COVERAGE.csv](PROFESSOR_TEMPLATE_COVERAGE.csv)

The inventory can be regenerated with
`Study Material/Tools/audit-repository.py`. Visual paper contact sheets can be
regenerated in the operating system's temporary directory with
`Study Material/Tools/render-exam-contact-sheets.py`.

## Where execution starts

There are not two independent `main` functions in the clean mixed project.
The path is:

```text
LPC1768 reset
  -> Source/startup_LPC17xx.s : Reset_Handler
  -> C runtime (__main)
  -> Source/exam/exam_main.c : int main(void)
  -> exam_init()
  -> Answer/exam_user.c : exam_user_init()
  -> forever: exam_user_loop(), exam_idle()
```

The C main is therefore:

`ARM_Exam_Project/Source/exam/exam_main.c`

The editable C answer is:

`ARM_Exam_Project/Answer/exam_user.c`

The editable assembly answer is:

`ARM_Exam_Project/Answer/exam_asm.s`

`exam_asm.s` exports `exam_asm_solution`; it does not define a second `main`.
For an ordinary Q1 routine, change the exported routine and call it from C by
declaring the matching `extern` prototype. For a paper that explicitly says to
write work in `Reset_Handler`, provide a strong `Reset_Handler`; the supplied
startup handler is weak so it can be replaced. Such an answer must still call
the C runtime if Q2 C code must run.

## Why Keil shows one directory

The Keil project intentionally contains one target named `ARM Exam` and one
visible group named `Answer Files`. The first three items are the answer files;
the remaining items are support files kept visible so the project can be built
without hidden dependencies.

There is no separate simulator source tree. The same linked LPC1768 image can
be selected for Keil's Cortex-M3 simulator or a physical debugger. That is a
reasonable exam layout, but it does **not** mean every LPC1768 peripheral is
accurately modeled by the generic Cortex-M3 simulator.

## Interrupt-vector ownership rule

The platform normally owns timer, RIT, SysTick, ADC and external-button
handlers so callbacks and debounce work. If the paper requires the handler
body itself, set exactly the corresponding flag to `1` in
`Source/platform/exam_config.h`, then define that handler in
`Answer/exam_user.c`.

Example for an answer that defines `TIMER1_IRQHandler` and `EINT0_IRQHandler`:

```c
#define EXAM_OWN_TIMER1_HANDLER 1
#define EXAM_OWN_EINT0_HANDLER  1
```

Do not use `exam_timer_every_ms()` for a timer whose vector you take over; the
callback helper deliberately returns busy when the built-in handler is absent.
Configure that timer with the lower-level match/start functions and clear its
write-one-to-clear interrupt flags inside the answer handler.

## Current API coverage

Against the 23 papers and the 15 professor templates, the clean project has the
needed reusable implementations for LEDs, INT0/KEY1/KEY2, debouncing,
joystick, timers 0–3, RIT, SysTick, ADC/potentiometer, DAC/speaker output,
event handoff, critical sections, SVC frame decoding, fault capture, AAPCS
integration and direct LPC1768 register access.

The exclusions are deliberate and historically supported:

- no CAN question in the 23-paper set;
- no MIDI/music-library question;
- no LCD, GLCD or touch question;
- no PCON exercise;
- no Ethernet template and no Ethernet exam question.

This means “full coverage” is valid only for the indexed exam history, not for
every possible LPC1768 peripheral.

## Known source defects and risks

### Incomplete historical answers

The following are not solutions: 2023-02-24 Q1; both questions for
2023-05-17, 2023-09-18, 2024-02-12, 2024-02-28, 2024-07-09 and 2024-09-16.
Their generic `exam_asm_example` and tutorial C must not be copied as answers.

### Affine transformation constant

The 29 January 2025 ARM1 paper specifies rows in the order
`F8, 7C, 3E, 1F, 8F, C7, E3, F1`. The historical C answer stores
`8F, C7, E3, F1, F8, 7C, 3E, 1F`. The assembly routine is structurally
reasonable, but the Q2 call uses the wrong matrix.

### Hofstadter-Conway length and RAM

The 18 February 2026 ARM2 paper requires 10,000 words. The answer defines
`SEQUENCE_LENGTH` as 1,000. Correcting it to 10,000 creates a single 40,000-byte
object, larger than either 32 KiB SRAM bank described by the current target.
This needs explicit memory placement or a linker arrangement that can satisfy
the paper; changing the constant alone is not a safe fix.

### Build versus correctness

A compiler accepting a routine does not prove signedness, output arrays,
callee-saved registers, stack restoration, public-boundary alignment, flags,
guard memory or termination. The existing Bulls and Cows lab has useful host
logic tests and a prior Keil build, but the repository still lacks the promised
automated linked-assembly Keil execution suite for every historical answer.

## Redundant files

Inside the submitted project, these are tool state rather than required source:

- `ARM_Exam_Template.uvguix.marwa` — per-user Keil window/debug state;
- `DebugConfig/ARM_Exam_LPC1768.dbgconf` — regenerable debugger configuration;
- `EventRecorderStub.scvd` — regenerable event-recorder stub;
- `ARM_Exam_Template.uvoptx` — useful shared debug/project options but not
  required to understand the answer source.

They are small and do not create a second code path. The `.uvprojx`, `Answer`,
`Source` and CMSIS files are not redundant. In particular, duplicated-looking
startup/system/CMSIS files are dependencies needed to keep the copied project
self-contained.

The restored `ARM`, `Architectures` and `Exams` directories intentionally
duplicate source study material outside this package. They are retained because
the USB handoff was explicitly required to contain them, and every copied file
was verified byte-for-byte.

## What can safely be claimed

You may say the clean project is a self-contained LPC1768 starting template
with one Keil target and broad historical peripheral coverage. Do not say that
all 23 solutions are complete, that all assembly was simulator-executed, or
that the board behavior was physically verified.


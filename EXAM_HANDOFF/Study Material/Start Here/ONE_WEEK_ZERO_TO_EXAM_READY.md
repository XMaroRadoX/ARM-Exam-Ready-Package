# One week from zero to ARM exam-ready

## The objective

The goal is not to memorize 23 finished answers. By exam day you should be able
to translate a paper into:

1. an exact assembly function contract;
2. a bounded algorithm using the correct loads, branches and stack discipline;
3. a small C state machine;
4. correct LPC1768 initialization and interrupt ownership;
5. a build-debug-submit sequence you have already rehearsed.

Use the clean project every day. Reading without writing code does not count as
practice.

## Daily rhythm

Use three focused blocks if possible:

- Block A, 90 minutes: learn one concept and reproduce its smallest example.
- Block B, 120 minutes: solve one paper section without looking at the answer.
- Block C, 60–90 minutes: build, debug, compare, and write a short error log.

Take a 10–15 minute break between blocks. At the end of each day, spend 20
minutes writing from memory: AAPCS rules, signed/unsigned branches, array address
formulas, and the interrupt-ownership rule.

## Day 1 - registers, memory and the project

Learn:

- R0–R3 arguments and R0 return value;
- caller-saved versus R4–R11 callee-saved;
- SP, LR, PC and APSR flags;
- byte versus word arrays;
- `LDR`, `STR`, `LDRB`, `STRB`, `LDRSB`;
- `MOV`, `ADD`, `SUB`, `CMP`, `B`, `BEQ`, `BNE`;
- the real project entry path.

Do:

1. Open `ARM_Exam_Project` and build the untouched project.
2. Put a breakpoint in C `main`, `exam_user_init`, and `exam_asm_solution`.
3. Change `exam_asm_solution` into `uint32_t add_three(uint32_t value)`.
4. Call it from `exam_user.c` and inspect R0 and LR.
5. Write a byte-array copy routine with source, destination and length.
6. Test lengths 0, 1 and 8 and place guard bytes around the destination.

Paper practice: 7 February 2023 Q1, first `copyData`, then signed insertion sort.

Ready-to-advance test:

- explain why a word-array index uses `LSL #2`;
- explain why signed bytes need `LDRSB`;
- show where C `main` and the assembly export are located without searching.

## Day 2 - flags, loops, AAPCS and nested calls

Learn:

- N, Z, C and V;
- signed branches `BLT/BGE/BLE/BGT`;
- unsigned branches `BLO/BHS/BLS/BHI`;
- `PUSH`, `POP`, `BL`, `BX LR`;
- leaf versus non-leaf routines;
- eight-byte public stack alignment;
- fifth and later arguments on the caller's stack;
- division and remainder with `UDIV` plus `MLS`.

Do:

1. Write a counted byte loop using `SUBS` and `BNE`.
2. Write a word-array maximum routine.
3. Convert it into a non-leaf routine that calls a helper.
4. Before each `BL`, calculate SP alignment on paper.
5. Write a five-argument C prototype and inspect the fifth argument in the
   debugger.
6. Work through one multiword add/subtract by hand using carry/no-borrow.

Paper practice: 4 July 2023 Q1 and either 29 January 2025 ARM2 or ARM3 Q1.

Ready-to-advance test:

- correctly choose `BLO` versus `BLT` for five examples;
- explain why LR must be saved before a nested `BL`;
- produce a balanced prologue/epilogue and restore SP exactly.

## Day 3 - recurring algorithm shapes

Learn and implement these shapes, not their filenames:

- nested scan and early break;
- recurrence written into a word array;
- decimal digit extraction using divide/remainder;
- run grouping and output construction;
- frequency arrays for duplicates;
- row-major matrix address calculation;
- graph/maze frontier or stack traversal.

Do:

1. Implement Recaman or Hofstadter Q from a C reference.
2. Implement Look-and-Say or RLE.
3. Implement Bulls and Cows frequency counting.
4. For each routine, write inputs, outputs, modified registers, element width,
   signedness, maximum iterations and memory size before coding.
5. Test zero/minimum, normal, duplicate-heavy and maximum configured inputs.

Paper practice: 3 February 2026 ARM1, ARM2 and ARM3 Q1. Use the atlas pattern
pages only after attempting each routine yourself.

Ready-to-advance test:

- derive `row * columns + column` and apply the byte/word scale;
- identify the exact loop bound that prevents an overrun;
- explain how Bulls and Cows avoids double-counting duplicates.

## Day 4 - GPIO, buttons, joystick and state machines

Learn:

- active-low inputs;
- LED number versus LED mask;
- edge versus current level;
- switch bounce and confirmation time;
- `volatile` interrupt-shared state;
- minimal interrupt/callback work;
- event flags and foreground state machines;
- one owner per interrupt vector.

Do:

1. Use `exam_buttons_start` to react to INT0, KEY1 and KEY2.
2. Use `exam_joystick_start` and record only press edges.
3. Build a three-state application: waiting, editing, showing result.
4. Repeat start/result/new-attempt transitions without resetting persistent
   state accidentally.
5. Then write one direct `EINT0_IRQHandler` exercise. Set
   `EXAM_OWN_EINT0_HANDLER` and confirm there is no duplicate symbol.

Main practice: the Bulls and Cows debug lab. Step through secret capture, four
digit edits, evaluation, another guess and the winning state.

Ready-to-advance test:

- explain why `current & changed` represents press edges;
- show the exact configuration change required before defining an EINT handler;
- keep a secret unchanged across multiple guesses.

## Day 5 - timers, RIT, SysTick, ADC and DAC

Learn:

- peripheral clock divider and timer clock;
- prescaler divides by `PR + 1`;
- match interrupt/reset/stop bits;
- periodic versus free-running versus one-shot behavior;
- write-one-to-clear interrupt flags;
- RIT/SysTick scheduling;
- 12-bit ADC and extracting the most significant eight bits;
- 10-bit DAC range;
- waveform-table index wrap.

Do:

1. Configure one 500 ms callback timer.
2. Configure one free-running timer with no interrupt and read its counter.
3. Configure a direct timer handler, including its ownership flag and W1C clear.
4. Convert ADC 0, 2048 and 4095 to the requested displayed byte.
5. Output a short DAC table and wrap the index without reading past the table.
6. Write timer calculations on paper before using the API.

Paper practice: 7 February 2023 Q2, 29 January 2025 one Q2 variant, and 3
February 2026 one Q2 variant.

Ready-to-advance test:

- calculate a match value from CCLK, PCLK divider, prescaler and period;
- distinguish reset-on-match from stopping a timer;
- explain why reading/clearing the wrong ADC register can lose a result.

## Day 6 - full timed mock exam

Choose a complete paper you have not just practiced. Recommended:

- 29 January 2025 ARM2 for matrix and timer work; or
- 3 February 2026 ARM3 for recurrence, ADC, button and timer work; or
- 25 June 2026 ARM1 for four-argument assembly and a state machine.

Run it under exam conditions:

1. Copy a fresh `ARM_Exam_Project` folder.
2. Do not edit the recovery copy.
3. Spend 15 minutes marking prototypes, resources, events, states and bounds.
4. Implement a callable Q1 stub first so Q2 can build.
5. Complete Q2 initialization and one event at a time.
6. Build after every milestone.
7. Use only the handbook, atlas and combined ARM library you will have on exam
   day.
8. Stop at the real time limit.
9. Reopen the saved project and perform the final checklist.

Afterward, classify every failure as one of: misunderstood requirement,
assembly syntax, ABI, vector ownership, peripheral calculation, state-machine
logic, memory bound, or submission procedure. Repair the weakest category, not
the easiest one.

## Day 7 - second mock, retrieval and USB rehearsal

Morning:

- reproduce AAPCS, flags, branch table, array scales and timer formulas from
  memory;
- locate five topics using PDF search and bookmarks;
- reproduce one byte loop, one word recurrence, one nested loop, one callback
  state machine and one direct IRQ skeleton.

Afternoon:

- take a second full paper from a different family;
- use a fresh copy of the submission project;
- require zero errors and inspect every warning;
- test boundary inputs before polishing comments.

Evening:

- copy the final `EXAM_HANDOFF` to the USB;
- verify that `ARM_Exam_Project`, `Study Material`, `ARM`, `Architectures` and
  `Exams` are present;
- open both new PDFs from the USB;
- open the Keil project from the USB copy;
- rehearse copying only `ARM_Exam_Project` into a fake exam folder;
- rehearse submitting only that copied project.

Stop heavy study early enough to sleep. The exam is dominated by careful
translation and debugging; sleep improves both more than one additional
unstructured paper.

## What to search during the exam

Use these exact queries:

| Need | Search term |
|---|---|
| signed byte array | `LDRSB` |
| unsigned loop bounds | `BLO/BHS` |
| nested assembly call | `non-leaf` or `BL` |
| fifth parameter | `stacked argument` |
| row-major matrix | `row-major` |
| decimal digits | `UDIV` or `MLS` |
| exact/partial matches | `frequency count` |
| direct IRQ collision | `EXAM_OWN_` |
| timer period | `prescaler` or `PR + 1` |
| ADC display byte | `most significant eight bits` |
| SVC handler | `stacked PC minus 2` |
| startup question | `Reset_Handler` |

## Minimum acceptable readiness

You are ready when you can complete all of the following without copying an
answer:

- a bounded assembly array routine that preserves R4-R11 and SP;
- a nested call with LR and alignment handled correctly;
- a signed and an unsigned loop with the correct branches;
- a timer calculation and handler with correct flag clearing;
- a debounced button or joystick state machine;
- an ADC-to-LED path and bounded DAC table loop;
- a fresh-project copy, build, reopen and submission rehearsal.


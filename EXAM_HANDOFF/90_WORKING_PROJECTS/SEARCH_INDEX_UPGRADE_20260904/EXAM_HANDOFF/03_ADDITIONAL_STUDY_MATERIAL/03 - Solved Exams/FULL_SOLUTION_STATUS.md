# Historical solution status

Compilation and solution completeness are separate checks. All 23 historical integrations build with the focused API. The seven former placeholder collections now contain question-specific C and assembly, but retain a build/reference status until their real linked assembly test harnesses pass in Keil's simulator.

## Exam-specific C and assembly present

- 2023-02-07 Sort and free-running timer
- 2023-07-04 Sociable numbers and timer
- 2025-01-29 ARM1 affine transformation
- 2025-01-29 ARM2 bit-matrix multiplication
- 2025-01-29 ARM3 transpose
- 2025-02-12 ARM1 sine/Maclaurin and DAC
- 2025-02-12 ARM2 cosine/Maclaurin and DAC
- 2025-07-01 ARM1 LCG rhythm
- 2025-07-01 ARM2 LCG rhythm
- 2026-02-03 ARM1 look-and-say and ADC
- 2026-02-03 ARM2 run-length encoding and ADC
- 2026-02-03 ARM3 Recaman, ADC, and timer
- 2026-02-18 ARM1 Hofstadter Q and three timers
- 2026-02-18 ARM2 Hofstadter-Conway and three timers
- 2026-06-25 ARM1 Bulls and Cows
- 2026-06-25 ARM2 Mastermind

These implementations assemble and link. Full semantic acceptance still requires execution of the ARM routines against independent vectors and ABI guard checks.

## Replaced placeholder implementations

- 2023-02-24 Kaprekar and SVC
- 2023-05-17 signed 64-bit division and flags
- 2023-09-18 digit addition and buttons
- 2024-02-12 maze, LCG, and timer
- 2024-02-28 shortest path and timer
- 2024-07-09 DFS and SysTick
- 2024-09-16 Kruskal and buttons

These folders now contain the required Kaprekar/SVC, signed 64-bit division/flags, digit-addition/buttons, maze/LCG, shortest-path/timer, DFS/SysTick, and Kruskal/buttons implementations. The independent C oracle suite passes and the new sources assemble and link at zero warnings. Their remaining acceptance gate is actual linked-assembly simulator execution with ABI and memory guards.

## Correctness labels

- `BUILD_PASS`: assembler/compiler/linker accepted the project.
- `HOST_REFERENCE_PASS`: an independent C oracle passed.
- `SIMULATOR_EXECUTED_PASS`: the linked ARM routine executed and passed output, memory-guard, register-preservation, SP-restoration, and termination checks.
- `PHYSICAL_BOARD_NOT_TESTED`: no electrical/physical claim.

No build-only project is described as fully correct.

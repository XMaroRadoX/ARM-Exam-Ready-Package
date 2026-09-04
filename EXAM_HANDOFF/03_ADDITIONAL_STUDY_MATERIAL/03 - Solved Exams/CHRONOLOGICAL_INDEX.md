# Historical ARM solutions: chronological index

Each directory contains a direct assembly answer, a direct C answer using the
easy `exam_*` API with native escape hatches where needed, source mapping,
adaptation notes, and verification evidence.
Search this page by algorithm, component, or date.

For detailed question-level searching, use the canonical
[past-exam search index](PAST_EXAM_SEARCH_INDEX.md). It has corrected tags for
algorithms, peripherals, events, timing, data layout, AAPCS and common risks.

| Date / variant | Q1 pattern | Q2 components | Solution |
|---|---|---|---|
| 2023-02-07 | signed-byte insertion sort | free-running timer, button | [Sort and timer](2023-02-07_Sort_FreeRunning_Timer/) |
| 2023-02-24 | Kaprekar recurrence/sorting | SVC and exception frame | [Kaprekar and SVC](2023-02-24_Kaprekar_SVC/) |
| 2023-05-17 | signed 64-bit division | result flags | [Signed 64-bit division](2023-05-17_Signed_64_Division/) |
| 2023-07-04 | sociable-number recurrence | timer | [Sociable and timer](2023-07-04_Sociable_Timer/) |
| 2023-09-18 | digit processing | multiple buttons | [Digit addition and buttons](2023-09-18_DigitAddition_Buttons/) |
| 2024-02-12 | maze and LCG | free-running timer | [Maze, LCG, timer](2024-02-12_Maze_LCG_Timer/) |
| 2024-02-28 | shortest path | periodic timer | [Shortest path and timer](2024-02-28_ShortestPath_Timer/) |
| 2024-07-09 | DFS | SysTick | [DFS and SysTick](2024-07-09_DFS_SysTick/) |
| 2024-09-16 | Kruskal/MST | button selection | [Kruskal and buttons](2024-09-16_Kruskal_Buttons/) |
| 2025-01-29 ARM1 | affine matrix operation | two timers | [Affine and timers](2025-01-29_ARM1_Affine_Two_Timers/) |
| 2025-01-29 ARM2 | packed/bit matrix | two timers | [Bit matrix and timers](2025-01-29_ARM2_Matrix_Two_Timers/) |
| 2025-01-29 ARM3 | transpose | timer | [Transpose and timer](2025-01-29_ARM3_Transpose_Timer/) |
| 2025-02-12 ARM1 | sine/Maclaurin, fixed point | DAC | [Sine and DAC](2025-02-12_ARM1_Sine_DAC/) |
| 2025-02-12 ARM2 | cosine/Maclaurin, fixed point | DAC | [Cosine and DAC](2025-02-12_ARM2_Cosine_DAC/) |
| 2025-07-01 ARM1 | LCG recurrence | timer rhythm | [LCG rhythm ARM1](2025-07-01_ARM1_LCG_Rhythm/) |
| 2025-07-01 ARM2 | LCG recurrence | timer rhythm | [LCG rhythm ARM2](2025-07-01_ARM2_LCG_Rhythm/) |
| 2026-02-03 ARM1 | Look-and-Say | ADC | [Look-and-Say and ADC](2026-02-03_ARM1_LookAndSay_ADC/) |
| 2026-02-03 ARM2 | run-length encoding | ADC | [RLE and ADC](2026-02-03_ARM2_RLE_ADC/) |
| 2026-02-03 ARM3 | Recaman | ADC and timer | [Recaman, ADC, timer](2026-02-03_ARM3_Recaman_ADC_Timer/) |
| 2026-02-18 ARM1 | Hofstadter Q | three timers | [Hofstadter Q](2026-02-18_ARM1_Three_Timers/) |
| 2026-02-18 ARM2 | Hofstadter-Conway, large array | three timers | [Hofstadter-Conway](2026-02-18_ARM2_Three_Timers/) |
| 2026-06-25 ARM1 | Bulls and Cows, duplicates | joystick, LEDs, free-running timer | [Bulls and Cows](2026-06-25_ARM1_BullsAndCows/) |
| 2026-06-25 ARM2 | Mastermind, duplicates | joystick, LEDs, free-running timer | [Mastermind](2026-06-25_ARM2_Mastermind/) |

## Search by component

Use the canonical [past-exam search index](PAST_EXAM_SEARCH_INDEX.md). It has
question-level tags for language, question type, algorithm, peripheral, event,
timing model, data shape, ABI concern and common risk. This chronological page
deliberately does not duplicate that changing search data.

## Status rule

`ARM_COMPILE_LINK_PASS` means the LPC1768 image assembled, compiled, and linked.
`SIMULATOR_EXECUTED_PASS` is used only when the linked ARM routine actually ran
and passed its output, ABI, stack, and guard-memory tests. No physical-board
claim is made without an attached board.

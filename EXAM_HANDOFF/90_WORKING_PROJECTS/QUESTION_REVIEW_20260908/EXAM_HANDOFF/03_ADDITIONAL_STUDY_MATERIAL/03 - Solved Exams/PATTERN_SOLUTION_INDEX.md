# Historical exam solution index

Use Ctrl+F with a keyword from the new question. Each **answer folder** contains the four expected source filenames, but the current audit found that seven early collections still contain placeholders. Read the status below before adapting anything.

Verification labels are literal. A present answer is not automatically a proven answer. Use the canonical workstation question page for the current compile and behavioral-test status.

## Verification warning

The seven former placeholder collections—2023-02-24, 2023-05-17, 2023-09-18, 2024-02-12, 2024-02-28, 2024-07-09, and 2024-09-16—now contain question-specific implementations and pass their Keil build plus independent C-oracle gates. They are still labeled build/reference verified until their real assembly symbols pass the complete simulator ABI and memory-guard suite. Never interpret file presence or compilation as simulator proof.

## Find by problem family

| Need | Closest worked answers |
|---|---|
| sorting / early break | 2023-02-07 Sort |
| digit sorting, recurrence, SVC | 2023-02-24 Kaprekar |
| signed or 64-bit division | 2023-05-17 Signed 64 Division |
| iterative number sequence | 2023-07-04 Sociable; 2026-02-03 Recamán |
| digit addition and buttons | 2023-09-18 Digit Addition |
| maze / DFS | 2024-02-12 Maze; 2024-07-09 DFS |
| shortest path / weighted graph | 2024-02-28 Shortest Path |
| Kruskal / edge sorting | 2024-09-16 Kruskal |
| affine transform / fixed point | 2025-01-29 ARM1 Affine |
| matrix traversal | 2025-01-29 ARM2 Matrix |
| transpose | 2025-01-29 ARM3 Transpose |
| sine/cosine and DAC | 2025-02-12 ARM1/ARM2 |
| LCG / rhythm / joystick | 2025-07-01 ARM1/ARM2 |
| Look-and-Say | 2026-02-03 ARM1 |
| run-length encoding | 2026-02-03 ARM2 |
| frequency tables / three timers | 2026-02-18 ARM1/ARM2 |
| Bulls and Cows / Mastermind | 2026-06-25 ARM1/ARM2 |

## All 23 answer folders

| Date / variant | Main assembly idea | Board idea | Answer folder |
|---|---|---|---|
| 2023-02-07 | sort, nested loops | free-running timer | [open](2023-02-07_Sort_FreeRunning_Timer/Answer%20Source) |
| 2023-02-24 | Kaprekar recurrence | SVC | [open](2023-02-24_Kaprekar_SVC/Answer%20Source) |
| 2023-05-17 | signed/wide division | ADC | [open](2023-05-17_Signed_64_Division/Answer%20Source) |
| 2023-07-04 | sociable recurrence | timer | [open](2023-07-04_Sociable_Timer/Answer%20Source) |
| 2023-09-18 | digit recurrence | buttons | [open](2023-09-18_DigitAddition_Buttons/Answer%20Source) |
| 2024-02-12 | maze/search/LCG | timer | [open](2024-02-12_Maze_LCG_Timer/Answer%20Source) |
| 2024-02-28 | shortest path | timer | [open](2024-02-28_ShortestPath_Timer/Answer%20Source) |
| 2024-07-09 | DFS | SysTick | [open](2024-07-09_DFS_SysTick/Answer%20Source) |
| 2024-09-16 | Kruskal | buttons | [open](2024-09-16_Kruskal_Buttons/Answer%20Source) |
| 2025-01-29 ARM1 | affine/fixed point | two timers | [open](2025-01-29_ARM1_Affine_Two_Timers/Answer%20Source) |
| 2025-01-29 ARM2 | matrix | two timers | [open](2025-01-29_ARM2_Matrix_Two_Timers/Answer%20Source) |
| 2025-01-29 ARM3 | transpose | timer | [open](2025-01-29_ARM3_Transpose_Timer/Answer%20Source) |
| 2025-02-12 ARM1 | fixed-point sine | ADC/DAC | [open](2025-02-12_ARM1_Sine_DAC/Answer%20Source) |
| 2025-02-12 ARM2 | fixed-point cosine | ADC/DAC | [open](2025-02-12_ARM2_Cosine_DAC/Answer%20Source) |
| 2025-07-01 ARM1 | LCG recurrence | rhythm/joystick | [open](2025-07-01_ARM1_LCG_Rhythm/Answer%20Source) |
| 2025-07-01 ARM2 | LCG recurrence | rhythm/joystick | [open](2025-07-01_ARM2_LCG_Rhythm/Answer%20Source) |
| 2026-02-03 ARM1 | Look-and-Say | ADC | [open](2026-02-03_ARM1_LookAndSay_ADC/Answer%20Source) |
| 2026-02-03 ARM2 | run-length encoding | ADC | [open](2026-02-03_ARM2_RLE_ADC/Answer%20Source) |
| 2026-02-03 ARM3 | Recamán | ADC/timer | [open](2026-02-03_ARM3_Recaman_ADC_Timer/Answer%20Source) |
| 2026-02-18 ARM1 | frequency/recurrence | three timers | [open](2026-02-18_ARM1_Three_Timers/Answer%20Source) |
| 2026-02-18 ARM2 | frequency/recurrence | three timers | [open](2026-02-18_ARM2_Three_Timers/Answer%20Source) |
| 2026-06-25 ARM1 | Bulls and Cows | joystick/game | [open](2026-06-25_ARM1_BullsAndCows/Answer%20Source) |
| 2026-06-25 ARM2 | Mastermind | joystick/game | [open](2026-06-25_ARM2_Mastermind/Answer%20Source) |

## Compare before copying

For a candidate answer, compare these six items with the new paper:

1. exact C/assembly prototype and argument order;
2. element width and signedness;
3. stopping condition and empty-input behavior;
4. output representation and sentinel values;
5. timer/vector/peripheral ownership;
6. restart and repeated-event requirements.

If any differs, use the pattern skeleton and adapt it deliberately instead of pasting the entire old answer.

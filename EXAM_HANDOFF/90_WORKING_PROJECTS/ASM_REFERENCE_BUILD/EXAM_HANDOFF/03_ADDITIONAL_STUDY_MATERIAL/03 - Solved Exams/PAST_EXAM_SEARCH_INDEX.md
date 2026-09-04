# Past-exam search index

This is the canonical way to search the 23 indexed ARM papers and their 48
questions. Use Ctrl+F with a tag such as `peripheral:adc`,
`algorithm:recaman`, `abi:stacked-arguments`, `event:key1`, or
`risk:debounce`. Tags describe only the question where the feature appears;
they are not inherited from the other question in the same paper.

## Fast searches

- Assembly contracts: `abi:`, `risk:stack-balance`, `data:`
- Algorithms: `algorithm:`
- Board work: `peripheral:`, `event:`, `timing:`
- Integration: `integration:c-calls-assembly`
- Exact input names: `int0`, `key1`, `key2`, `joystick`, `systick`
- Verification status remains on each exam card and solved answer.

## Tag vocabulary

| Prefix | Meaning | Example |
|---|---|---|
| `lang:` | Language you must write | `lang:assembly` |
| `type:` | Shape of the question | `type:c-board-integration` |
| `algorithm:` | Required method | `algorithm:run-length-encoding` |
| `peripheral:` | LPC1768/board component | `peripheral:timer1` |
| `event:` | Callback, interrupt or input source | `event:int0` |
| `timing:` | Timer behavior/period | `timing:free-running-seed` |
| `data:` | Element width and layout | `data:packed-8x8-bit-matrix` |
| `abi:` | AAPCS/call requirement | `abi:stacked-arguments` |
| `risk:` | Likely failure point | `risk:operator-precedence` |

## All questions

| Question | Mode | Algorithms / data | Board / events / timing | ABI / risks | Answer |
|---|---|---|---|---|---|
| [E2023-02-07-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-02-07/EXAM_CARD.md) | assembly-algorithm | array-copy, insertion-sort, signed-byte-array, read-only-input, writable-output | - | non-leaf, callee-saved-registers, signedness, bounds, stack-balance | [2023-02-07_Sort_FreeRunning_Timer](2023-02-07_Sort_FreeRunning_Timer/) |
| [E2023-02-07-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-02-07/EXAM_CARD.md) | c-board-integration | capture-and-sort, signed-byte-array | led, timer1, buttons, int0, key1, free-running, reset-at-match-no-irq | c-calls-assembly, debounce, irq-shared-state, timer-ownership, vector-ownership | [2023-02-07_Sort_FreeRunning_Timer](2023-02-07_Sort_FreeRunning_Timer/) |
| [E2023-02-24-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-02-24/EXAM_CARD.md) | assembly-algorithm | kaprekar, decimal-digits, sorting, recurrence, scalar, digit-array | - | non-leaf, callee-saved-registers, signedness, termination, stack-balance | [2023-02-24_Kaprekar_SVC](2023-02-24_Kaprekar_SVC/) |
| [E2023-02-24-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-02-24/EXAM_CARD.md) | assembly-exception | kaprekar-iteration, exception-frame | svc-50 | non-leaf, exception-return, callee-saved-registers, msp-vs-psp, svc-decode, stack-balance | [2023-02-24_Kaprekar_SVC](2023-02-24_Kaprekar_SVC/) |
| [E2023-05-17-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-05-17/EXAM_CARD.md) | assembly-algorithm | signed-restoring-division, signed-64-bit, two-word-value, signed-32-bit | - | two-register-wide-input, callee-saved-registers, divide-by-zero, sign-normalization, overflow, stack-balance | [2023-05-17_Signed_64_Division](2023-05-17_Signed_64_Division/) |
| [E2023-05-17-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-05-17/EXAM_CARD.md) | assembly-flags | condition-flag-result, apsr-flags | - | flags-return-contract, nzcv-semantics | [2023-05-17_Signed_64_Division](2023-05-17_Signed_64_Division/) |
| [E2023-07-04-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-07-04/EXAM_CARD.md) | assembly-algorithm | aliquot-sum, sociable-sequence, divisor-search, recurrence, word-array | - | non-leaf, callee-saved-registers, termination, division, stack-balance | [2023-07-04_Sociable_Timer](2023-07-04_Sociable_Timer/) |
| [E2023-07-04-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-07-04/EXAM_CARD.md) | c-board-integration | circular-sequence, word-array | led, timer1, timer-interrupt, periodic-2-seconds | c-calls-assembly, irq-shared-state, timer-ownership | [2023-07-04_Sociable_Timer](2023-07-04_Sociable_Timer/) |
| [E2023-09-18-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-09-18/EXAM_CARD.md) | assembly-algorithm | digit-sum, digit-addition, decimal-digits, scalar, digit-array | - | non-leaf, callee-saved-registers, arithmetic-overflow, stack-balance | [2023-09-18_DigitAddition_Buttons](2023-09-18_DigitAddition_Buttons/) |
| [E2023-09-18-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2023/2023-09-18/EXAM_CARD.md) | c-board-integration | binary-value-construction, array-comparison, word-array | led, buttons, int0, key1, key2 | c-calls-assembly, debounce, irq-shared-state | [2023-09-18_DigitAddition_Buttons](2023-09-18_DigitAddition_Buttons/) |
| [E2024-02-12-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-02-12/EXAM_CARD.md) | assembly-algorithm | maze-propagation, flood-fill, graph-search, byte-matrix, row-major | - | callee-saved-registers, bounds, no-progress-termination, stack-balance | [2024-02-12_Maze_LCG_Timer](2024-02-12_Maze_LCG_Timer/) |
| [E2024-02-12-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-02-12/EXAM_CARD.md) | c-board-integration | lcg, maze-generation, byte-matrix, row-major | led, timer0, buttons, key2, free-running-seed | c-calls-assembly, debounce, bounds, irq-shared-state, timer-ownership | [2024-02-12_Maze_LCG_Timer](2024-02-12_Maze_LCG_Timer/) |
| [E2024-02-28-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-02-28/EXAM_CARD.md) | assembly-algorithm | unweighted-shortest-path, maze-propagation, byte-matrix, row-major | - | callee-saved-registers, bounds, unreachable-destination, stack-balance | [2024-02-28_ShortestPath_Timer](2024-02-28_ShortestPath_Timer/) |
| [E2024-02-28-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-02-28/EXAM_CARD.md) | c-board-state-machine | led-sequence | led, timer, timer-interrupt, periodic-500-ms | callback, irq-shared-state, timer-ownership, lost-events | [2024-02-28_ShortestPath_Timer](2024-02-28_ShortestPath_Timer/) |
| [E2024-07-09-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-07-09/EXAM_CARD.md) | assembly-algorithm | depth-first-search, explicit-stack, maze, byte-matrix, row-major, explicit-stack | - | four-register-arguments, non-leaf, callee-saved-registers, stack-capacity, bounds, stack-balance | [2024-07-09_DFS_SysTick](2024-07-09_DFS_SysTick/) |
| [E2024-07-09-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-07-09/EXAM_CARD.md) | assembly-startup-exception | available-moves, modulo-selection, byte-matrix, candidate-array | systick, systick-interrupt, periodic | reset-handler, non-leaf, direct-register-setup, stack-balance, vector-ownership | [2024-07-09_DFS_SysTick](2024-07-09_DFS_SysTick/) |
| [E2024-09-16-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-09-16/EXAM_CARD.md) | assembly-algorithm | kruskal, component-label-merge, min-max-reduction, three-word-arrays, row-major | - | seven-arguments, stacked-arguments, non-leaf, callee-saved-registers, stacked-offsets, bounds, stack-balance | [2024-09-16_Kruskal_Buttons](2024-09-16_Kruskal_Buttons/) |
| [E2024-09-16-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2024/2024-09-16/EXAM_CARD.md) | c-board-state-machine | button-ordered-offset | led, buttons, int0, key1, key2 | callback, debounce, event-order, irq-shared-state | [2024-09-16_Kruskal_Buttons](2024-09-16_Kruskal_Buttons/) |
| [E2025-01-29-A1-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-01-29-A1/EXAM_CARD.md) | assembly-algorithm | bitwise-affine-transform, packed-matrix, packed-8x8-bit-matrix, byte-array | - | callee-saved-registers, bit-order, row-order, bounds, stack-balance | [2025-01-29_ARM1_Affine_Two_Timers](2025-01-29_ARM1_Affine_Two_Timers/) |
| [E2025-01-29-A1-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-01-29-A1/EXAM_CARD.md) | c-board-integration | byte-capture, xor, row-display, byte-array, packed-8x8-bit-matrix | led, timer0, timer1, buttons, int0, key1, timer0-interrupt, free-running, periodic-500-ms-full-cycle | c-calls-assembly, debounce, irq-shared-state, timer-ownership | [2025-01-29_ARM1_Affine_Two_Timers](2025-01-29_ARM1_Affine_Two_Timers/) |
| [E2025-01-29-A2-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-01-29-A2/EXAM_CARD.md) | assembly-algorithm | binary-matrix-multiplication, bit-dot-product, packed-8x8-bit-matrix, byte-array | - | callee-saved-registers, bit-order, bounds, stack-balance | [2025-01-29_ARM2_Matrix_Two_Timers](2025-01-29_ARM2_Matrix_Two_Timers/) |
| [E2025-01-29-A2-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-01-29-A2/EXAM_CARD.md) | c-board-integration | matrix-capture, row-display, two-packed-matrices, output-matrix | led, timer0, timer1, buttons, int0, key1, timer0-interrupt, free-running, periodic-500-ms | c-calls-assembly, debounce, irq-shared-state, timer-ownership | [2025-01-29_ARM2_Matrix_Two_Timers](2025-01-29_ARM2_Matrix_Two_Timers/) |
| [E2025-01-29-A3-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-01-29-A3/EXAM_CARD.md) | assembly-algorithm | packed-matrix-transpose, packed-8x8-bit-matrix, byte-array, read-only-input, writable-output | - | two-pointer-arguments, callee-saved-registers, msb-first-bit-order, bounds, stack-balance | [2025-01-29_ARM3_Transpose_Timer](2025-01-29_ARM3_Transpose_Timer/) |
| [E2025-01-29-A3-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-01-29-A3/EXAM_CARD.md) | c-board-integration | array-capture, xor-equivalence, five-byte-arrays, packed-8x8-bit-matrices | led, timer2, buttons, int0, key1, key2, free-running-reset-at-0xffff-no-irq | c-calls-assembly-three-times, debounce, bounds, irq-shared-state, timer-ownership | [2025-01-29_ARM3_Transpose_Timer](2025-01-29_ARM3_Transpose_Timer/) |
| [E2025-02-12-A1-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-02-12-A1/EXAM_CARD.md) | assembly-algorithm | sine-maclaurin, fixed-point-recurrence, signed-word-array, sample-table | - | non-leaf, callee-saved-registers, fixed-point-scale, signedness, overflow, bounds, stack-balance | [2025-02-12_ARM1_Sine_DAC](2025-02-12_ARM1_Sine_DAC/) |
| [E2025-02-12-A1-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-02-12-A1/EXAM_CARD.md) | c-board-integration | waveform-generation, sample-streaming, sine-table-45 | dac, timer0, buttons, speaker, int0, timer0-interrupt, periodic-1263-cycles | c-calls-assembly, irq-shared-state, timer-ownership, sample-bounds | [2025-02-12_ARM1_Sine_DAC](2025-02-12_ARM1_Sine_DAC/) |
| [E2025-02-12-A2-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-02-12-A2/EXAM_CARD.md) | assembly-algorithm | cosine-maclaurin, fixed-point-recurrence, signed-word-array, sample-table | - | non-leaf, callee-saved-registers, fixed-point-scale, signedness, overflow, bounds, stack-balance | [2025-02-12_ARM2_Cosine_DAC](2025-02-12_ARM2_Cosine_DAC/) |
| [E2025-02-12-A2-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-02-12-A2/EXAM_CARD.md) | c-board-integration | waveform-generation, sample-streaming, cosine-table | dac, timer1, buttons, speaker, key1, timer1-interrupt, periodic-1592-cycles | c-calls-assembly, debounce, irq-shared-state, timer-ownership, sample-bounds | [2025-02-12_ARM2_Cosine_DAC](2025-02-12_ARM2_Cosine_DAC/) |
| [E2025-07-01-A1-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-07-01-A1/EXAM_CARD.md) | assembly-algorithm | linear-congruential-generator, modulo, unsigned-word-state | - | five-arguments, stacked-argument, callee-saved-registers, unsigned-wrap, divide-by-zero, stacked-offset, stack-balance | [2025-07-01_ARM1_LCG_Rhythm](2025-07-01_ARM1_LCG_Rhythm/) |
| [E2025-07-01-A1-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-07-01-A1/EXAM_CARD.md) | assembly-startup | lcg-sequence, recurrence, word-array, persistent-state | - | reset-handler, non-leaf, five-arguments, stack-alignment, stacked-arguments, non-returning-loop | [2025-07-01_ARM1_LCG_Rhythm](2025-07-01_ARM1_LCG_Rhythm/) |
| [E2025-07-01-A1-Q3](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-07-01-A1/EXAM_CARD.md) | c-board-state-machine | rhythm-game, first-input-only | led, timer0, joystick, joystick-first-movement, timer0-interrupt, periodic-3-seconds | callback, debounce, first-event-latching, irq-shared-state, timer-ownership | [2025-07-01_ARM1_LCG_Rhythm](2025-07-01_ARM1_LCG_Rhythm/) |
| [E2025-07-01-A2-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-07-01-A2/EXAM_CARD.md) | assembly-algorithm | linear-congruential-generator, modulo, shift, unsigned-word-state | - | five-arguments, stacked-argument, callee-saved-registers, unsigned-wrap, shift-range, stacked-offset, stack-balance | [2025-07-01_ARM2_LCG_Rhythm](2025-07-01_ARM2_LCG_Rhythm/) |
| [E2025-07-01-A2-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-07-01-A2/EXAM_CARD.md) | assembly-startup | lcg-sequence, recurrence, shift, word-array, persistent-state | - | reset-handler, non-leaf, five-arguments, stack-alignment, stacked-arguments, non-returning-loop | [2025-07-01_ARM2_LCG_Rhythm](2025-07-01_ARM2_LCG_Rhythm/) |
| [E2025-07-01-A2-Q3](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2025/2025-07-01-A2/EXAM_CARD.md) | c-board-state-machine | rhythm-game, first-input-only | led, timer1, joystick, joystick-first-movement, timer1-interrupt, periodic-2.5-seconds | callback, debounce, first-event-latching, irq-shared-state, timer-ownership | [2025-07-01_ARM2_LCG_Rhythm](2025-07-01_ARM2_LCG_Rhythm/) |
| [E2026-02-03-A1-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-03-A1/EXAM_CARD.md) | assembly-algorithm | look-and-say, run-grouping, bounded-output, digit-byte-array, output-buffer | - | non-leaf, callee-saved-registers, capacity, final-run, bounds, stack-balance | [2026-02-03_ARM1_LookAndSay_ADC](2026-02-03_ARM1_LookAndSay_ADC/) |
| [E2026-02-03-A1-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-03-A1/EXAM_CARD.md) | c-board-integration | adc-display, sequence-generation, adc-12-bit, byte-array | adc, potentiometer, led, buttons, int0, adc-complete | c-calls-assembly, debounce, irq-shared-state, adc-channel, bounds | [2026-02-03_ARM1_LookAndSay_ADC](2026-02-03_ARM1_LookAndSay_ADC/) |
| [E2026-02-03-A2-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-03-A2/EXAM_CARD.md) | assembly-algorithm | run-length-encoding, run-grouping, digit-byte-array, count-value-output | - | callee-saved-registers, capacity, final-run, bounds, stack-balance | [2026-02-03_ARM2_RLE_ADC](2026-02-03_ARM2_RLE_ADC/) |
| [E2026-02-03-A2-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-03-A2/EXAM_CARD.md) | c-board-integration | adc-display, run-length-encoding, adc-12-bit, byte-array | adc, potentiometer, led, buttons, key1, adc-complete | c-calls-assembly, debounce, irq-shared-state, adc-channel, bounds | [2026-02-03_ARM2_RLE_ADC](2026-02-03_ARM2_RLE_ADC/) |
| [E2026-02-03-A3-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-03-A3/EXAM_CARD.md) | assembly-algorithm | recaman, indirect-recurrence, duplicate-search, word-array | - | non-leaf, callee-saved-registers, duplicate-detection, positive-subtraction, bounds, stack-balance | [2026-02-03_ARM3_Recaman_ADC_Timer](2026-02-03_ARM3_Recaman_ADC_Timer/) |
| [E2026-02-03-A3-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-03-A3/EXAM_CARD.md) | c-board-integration | adc-display, sequence-display, adc-12-bit, word-array | adc, potentiometer, led, timer, buttons, key2, timer-interrupt, adc-complete, periodic-2-seconds | c-calls-assembly, debounce, irq-shared-state, adc-channel, timer-ownership, bounds | [2026-02-03_ARM3_Recaman_ADC_Timer](2026-02-03_ARM3_Recaman_ADC_Timer/) |
| [E2026-02-18-A1-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-18-A1/EXAM_CARD.md) | assembly-algorithm | hofstadter-q, indirect-recurrence, maximum-reduction, word-array-1000 | - | two-arguments, callee-saved-registers, one-based-vs-zero-based, indirect-index, bounds, stack-balance | [2026-02-18_ARM1_Three_Timers](2026-02-18_ARM1_Three_Timers/) |
| [E2026-02-18-A1-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-18-A1/EXAM_CARD.md) | c-board-integration | frequency-scaling, duration-scaling, sample-streaming, word-array-1000, sine-table-45, uint16-samples | dac, speaker, timer-a, timer-b, timer-c, three-timer-interrupts, scheduler-50-ms, periodic-sample-rate, one-shot-duration | c-calls-assembly, overflow-order, irq-shared-state, three-timer-ownership, sample-wrap, running-state | [2026-02-18_ARM1_Three_Timers](2026-02-18_ARM1_Three_Timers/) |
| [E2026-02-18-A2-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-18-A2/EXAM_CARD.md) | assembly-algorithm | hofstadter-conway, indirect-recurrence, maximum-reduction, word-array-10000-declared, first-1000-used | - | two-arguments, callee-saved-registers, one-based-vs-zero-based, indirect-index, large-static-array, bounds, stack-balance | [2026-02-18_ARM2_Three_Timers](2026-02-18_ARM2_Three_Timers/) |
| [E2026-02-18-A2-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-02-18-A2/EXAM_CARD.md) | c-board-integration | frequency-scaling, duration-scaling, sample-streaming, word-array-1000, sine-table-45, uint16-samples | dac, speaker, timer-a, timer-b, timer-c, three-timer-interrupts, scheduler-50-ms, periodic-sample-rate, one-shot-duration | c-calls-assembly, overflow-order, irq-shared-state, three-timer-ownership, sample-wrap, running-state | [2026-02-18_ARM2_Three_Timers](2026-02-18_ARM2_Three_Timers/) |
| [E2026-06-25-B1-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-06-25-B1/EXAM_CARD.md) | assembly-algorithm | bulls-and-cows, frequency-count, duplicate-safe-matching, min-reduction, four-word-arrays, four-digits | - | four-register-arguments, callee-saved-registers, duplicates, zero-initialization, operator-precedence, stack-balance | [2026-06-25_ARM1_BullsAndCows](2026-06-25_ARM1_BullsAndCows/) |
| [E2026-06-25-B1-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-06-25-B1/EXAM_CARD.md) | c-board-integration | game-state-machine, timer-derived-secret, bitfield-display, four-word-arrays, four-two-bit-fields | led, timer, joystick, joystick-select, joystick-directions, free-running-seed | c-calls-assembly, debounce, secret-lifetime, state-transition, irq-shared-state, timer-ownership | [2026-06-25_ARM1_BullsAndCows](2026-06-25_ARM1_BullsAndCows/) |
| [E2026-06-25-B2-Q1](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-06-25-B2/EXAM_CARD.md) | assembly-algorithm | mastermind, consume-once-matching, nested-search, early-break, four-word-arrays, used-marker-arrays | - | four-register-arguments, callee-saved-registers, duplicates, zero-initialization, operator-precedence, stack-balance | [2026-06-25_ARM2_Mastermind](2026-06-25_ARM2_Mastermind/) |
| [E2026-06-25-B2-Q2](../04%20-%20Reference/Atlas%20Data%20and%20Indexes/ARM_EXAM_ATLAS/exams/2026/2026-06-25-B2/EXAM_CARD.md) | c-board-integration | game-state-machine, timer-derived-secret, bitfield-display, four-word-arrays, four-two-bit-fields | led, timer, joystick, joystick-select, joystick-directions, free-running-seed | c-calls-assembly, debounce, secret-lifetime, state-transition, irq-shared-state, timer-ownership | [2026-06-25_ARM2_Mastermind](2026-06-25_ARM2_Mastermind/) |

## Exact tag groups

Every tag below is searchable verbatim. Question IDs link through the table above.

### Algorithm tags

- `algorithm:adc-display` - E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2
- `algorithm:aliquot-sum` - E2023-07-04-Q1
- `algorithm:array-capture` - E2025-01-29-A3-Q2
- `algorithm:array-comparison` - E2023-09-18-Q2
- `algorithm:array-copy` - E2023-02-07-Q1
- `algorithm:available-moves` - E2024-07-09-Q2
- `algorithm:binary-matrix-multiplication` - E2025-01-29-A2-Q1
- `algorithm:binary-value-construction` - E2023-09-18-Q2
- `algorithm:bit-dot-product` - E2025-01-29-A2-Q1
- `algorithm:bitfield-display` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `algorithm:bitwise-affine-transform` - E2025-01-29-A1-Q1
- `algorithm:bounded-output` - E2026-02-03-A1-Q1
- `algorithm:bulls-and-cows` - E2026-06-25-B1-Q1
- `algorithm:button-ordered-offset` - E2024-09-16-Q2
- `algorithm:byte-capture` - E2025-01-29-A1-Q2
- `algorithm:capture-and-sort` - E2023-02-07-Q2
- `algorithm:circular-sequence` - E2023-07-04-Q2
- `algorithm:component-label-merge` - E2024-09-16-Q1
- `algorithm:condition-flag-result` - E2023-05-17-Q2
- `algorithm:consume-once-matching` - E2026-06-25-B2-Q1
- `algorithm:cosine-maclaurin` - E2025-02-12-A2-Q1
- `algorithm:decimal-digits` - E2023-02-24-Q1, E2023-09-18-Q1
- `algorithm:depth-first-search` - E2024-07-09-Q1
- `algorithm:digit-addition` - E2023-09-18-Q1
- `algorithm:digit-sum` - E2023-09-18-Q1
- `algorithm:divisor-search` - E2023-07-04-Q1
- `algorithm:duplicate-safe-matching` - E2026-06-25-B1-Q1
- `algorithm:duplicate-search` - E2026-02-03-A3-Q1
- `algorithm:duration-scaling` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `algorithm:early-break` - E2026-06-25-B2-Q1
- `algorithm:explicit-stack` - E2024-07-09-Q1
- `algorithm:first-input-only` - E2025-07-01-A1-Q3, E2025-07-01-A2-Q3
- `algorithm:fixed-point-recurrence` - E2025-02-12-A1-Q1, E2025-02-12-A2-Q1
- `algorithm:flood-fill` - E2024-02-12-Q1
- `algorithm:frequency-count` - E2026-06-25-B1-Q1
- `algorithm:frequency-scaling` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `algorithm:game-state-machine` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `algorithm:graph-search` - E2024-02-12-Q1
- `algorithm:hofstadter-conway` - E2026-02-18-A2-Q1
- `algorithm:hofstadter-q` - E2026-02-18-A1-Q1
- `algorithm:indirect-recurrence` - E2026-02-03-A3-Q1, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1
- `algorithm:insertion-sort` - E2023-02-07-Q1
- `algorithm:kaprekar` - E2023-02-24-Q1
- `algorithm:kaprekar-iteration` - E2023-02-24-Q2
- `algorithm:kruskal` - E2024-09-16-Q1
- `algorithm:lcg` - E2024-02-12-Q2
- `algorithm:lcg-sequence` - E2025-07-01-A1-Q2, E2025-07-01-A2-Q2
- `algorithm:led-sequence` - E2024-02-28-Q2
- `algorithm:linear-congruential-generator` - E2025-07-01-A1-Q1, E2025-07-01-A2-Q1
- `algorithm:look-and-say` - E2026-02-03-A1-Q1
- `algorithm:mastermind` - E2026-06-25-B2-Q1
- `algorithm:matrix-capture` - E2025-01-29-A2-Q2
- `algorithm:maximum-reduction` - E2026-02-18-A1-Q1, E2026-02-18-A2-Q1
- `algorithm:maze` - E2024-07-09-Q1
- `algorithm:maze-generation` - E2024-02-12-Q2
- `algorithm:maze-propagation` - E2024-02-12-Q1, E2024-02-28-Q1
- `algorithm:min-max-reduction` - E2024-09-16-Q1
- `algorithm:min-reduction` - E2026-06-25-B1-Q1
- `algorithm:modulo` - E2025-07-01-A1-Q1, E2025-07-01-A2-Q1
- `algorithm:modulo-selection` - E2024-07-09-Q2
- `algorithm:nested-search` - E2026-06-25-B2-Q1
- `algorithm:packed-matrix` - E2025-01-29-A1-Q1
- `algorithm:packed-matrix-transpose` - E2025-01-29-A3-Q1
- `algorithm:recaman` - E2026-02-03-A3-Q1
- `algorithm:recurrence` - E2023-02-24-Q1, E2023-07-04-Q1, E2025-07-01-A1-Q2, E2025-07-01-A2-Q2
- `algorithm:rhythm-game` - E2025-07-01-A1-Q3, E2025-07-01-A2-Q3
- `algorithm:row-display` - E2025-01-29-A1-Q2, E2025-01-29-A2-Q2
- `algorithm:run-grouping` - E2026-02-03-A1-Q1, E2026-02-03-A2-Q1
- `algorithm:run-length-encoding` - E2026-02-03-A2-Q1, E2026-02-03-A2-Q2
- `algorithm:sample-streaming` - E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `algorithm:sequence-display` - E2026-02-03-A3-Q2
- `algorithm:sequence-generation` - E2026-02-03-A1-Q2
- `algorithm:shift` - E2025-07-01-A2-Q1, E2025-07-01-A2-Q2
- `algorithm:signed-restoring-division` - E2023-05-17-Q1
- `algorithm:sine-maclaurin` - E2025-02-12-A1-Q1
- `algorithm:sociable-sequence` - E2023-07-04-Q1
- `algorithm:sorting` - E2023-02-24-Q1
- `algorithm:timer-derived-secret` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `algorithm:unweighted-shortest-path` - E2024-02-28-Q1
- `algorithm:waveform-generation` - E2025-02-12-A1-Q2, E2025-02-12-A2-Q2
- `algorithm:xor` - E2025-01-29-A1-Q2
- `algorithm:xor-equivalence` - E2025-01-29-A3-Q2

### Peripheral tags

- `peripheral:adc` - E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2
- `peripheral:buttons` - E2023-02-07-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2
- `peripheral:dac` - E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `peripheral:joystick` - E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `peripheral:led` - E2023-02-07-Q2, E2023-07-04-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-02-28-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `peripheral:potentiometer` - E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2
- `peripheral:speaker` - E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `peripheral:systick` - E2024-07-09-Q2
- `peripheral:timer` - E2024-02-28-Q2, E2026-02-03-A3-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `peripheral:timer-a` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `peripheral:timer-b` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `peripheral:timer-c` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `peripheral:timer0` - E2024-02-12-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-02-12-A1-Q2, E2025-07-01-A1-Q3
- `peripheral:timer1` - E2023-02-07-Q2, E2023-07-04-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-02-12-A2-Q2, E2025-07-01-A2-Q3
- `peripheral:timer2` - E2025-01-29-A3-Q2

### Event tags

- `event:adc-complete` - E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2
- `event:int0` - E2023-02-07-Q2, E2023-09-18-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2026-02-03-A1-Q2
- `event:joystick-directions` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `event:joystick-first-movement` - E2025-07-01-A1-Q3, E2025-07-01-A2-Q3
- `event:joystick-select` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `event:key1` - E2023-02-07-Q2, E2023-09-18-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A2-Q2, E2026-02-03-A2-Q2
- `event:key2` - E2023-09-18-Q2, E2024-02-12-Q2, E2024-09-16-Q2, E2025-01-29-A3-Q2, E2026-02-03-A3-Q2
- `event:svc-50` - E2023-02-24-Q2
- `event:systick-interrupt` - E2024-07-09-Q2
- `event:three-timer-interrupts` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `event:timer-interrupt` - E2023-07-04-Q2, E2024-02-28-Q2, E2026-02-03-A3-Q2
- `event:timer0-interrupt` - E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-02-12-A1-Q2, E2025-07-01-A1-Q3
- `event:timer1-interrupt` - E2025-02-12-A2-Q2, E2025-07-01-A2-Q3

### Timing tags

- `timing:free-running` - E2023-02-07-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2
- `timing:free-running-reset-at-0xffff-no-irq` - E2025-01-29-A3-Q2
- `timing:free-running-seed` - E2024-02-12-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `timing:one-shot-duration` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `timing:periodic` - E2024-07-09-Q2
- `timing:periodic-1263-cycles` - E2025-02-12-A1-Q2
- `timing:periodic-1592-cycles` - E2025-02-12-A2-Q2
- `timing:periodic-2-seconds` - E2023-07-04-Q2, E2026-02-03-A3-Q2
- `timing:periodic-2.5-seconds` - E2025-07-01-A2-Q3
- `timing:periodic-3-seconds` - E2025-07-01-A1-Q3
- `timing:periodic-500-ms` - E2024-02-28-Q2, E2025-01-29-A2-Q2
- `timing:periodic-500-ms-full-cycle` - E2025-01-29-A1-Q2
- `timing:periodic-sample-rate` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `timing:reset-at-match-no-irq` - E2023-02-07-Q2
- `timing:scheduler-50-ms` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2

### Data tags

- `data:adc-12-bit` - E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2
- `data:apsr-flags` - E2023-05-17-Q2
- `data:byte-array` - E2025-01-29-A1-Q1, E2025-01-29-A1-Q2, E2025-01-29-A2-Q1, E2025-01-29-A3-Q1, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2
- `data:byte-matrix` - E2024-02-12-Q1, E2024-02-12-Q2, E2024-02-28-Q1, E2024-07-09-Q1, E2024-07-09-Q2
- `data:candidate-array` - E2024-07-09-Q2
- `data:cosine-table` - E2025-02-12-A2-Q2
- `data:count-value-output` - E2026-02-03-A2-Q1
- `data:digit-array` - E2023-02-24-Q1, E2023-09-18-Q1
- `data:digit-byte-array` - E2026-02-03-A1-Q1, E2026-02-03-A2-Q1
- `data:exception-frame` - E2023-02-24-Q2
- `data:explicit-stack` - E2024-07-09-Q1
- `data:first-1000-used` - E2026-02-18-A2-Q1
- `data:five-byte-arrays` - E2025-01-29-A3-Q2
- `data:four-digits` - E2026-06-25-B1-Q1
- `data:four-two-bit-fields` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `data:four-word-arrays` - E2026-06-25-B1-Q1, E2026-06-25-B1-Q2, E2026-06-25-B2-Q1, E2026-06-25-B2-Q2
- `data:output-buffer` - E2026-02-03-A1-Q1
- `data:output-matrix` - E2025-01-29-A2-Q2
- `data:packed-8x8-bit-matrices` - E2025-01-29-A3-Q2
- `data:packed-8x8-bit-matrix` - E2025-01-29-A1-Q1, E2025-01-29-A1-Q2, E2025-01-29-A2-Q1, E2025-01-29-A3-Q1
- `data:persistent-state` - E2025-07-01-A1-Q2, E2025-07-01-A2-Q2
- `data:read-only-input` - E2023-02-07-Q1, E2025-01-29-A3-Q1
- `data:row-major` - E2024-02-12-Q1, E2024-02-12-Q2, E2024-02-28-Q1, E2024-07-09-Q1, E2024-09-16-Q1
- `data:sample-table` - E2025-02-12-A1-Q1, E2025-02-12-A2-Q1
- `data:scalar` - E2023-02-24-Q1, E2023-09-18-Q1
- `data:signed-32-bit` - E2023-05-17-Q1
- `data:signed-64-bit` - E2023-05-17-Q1
- `data:signed-byte-array` - E2023-02-07-Q1, E2023-02-07-Q2
- `data:signed-word-array` - E2025-02-12-A1-Q1, E2025-02-12-A2-Q1
- `data:sine-table-45` - E2025-02-12-A1-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `data:three-word-arrays` - E2024-09-16-Q1
- `data:two-packed-matrices` - E2025-01-29-A2-Q2
- `data:two-word-value` - E2023-05-17-Q1
- `data:uint16-samples` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `data:unsigned-word-state` - E2025-07-01-A1-Q1, E2025-07-01-A2-Q1
- `data:used-marker-arrays` - E2026-06-25-B2-Q1
- `data:word-array` - E2023-07-04-Q1, E2023-07-04-Q2, E2023-09-18-Q2, E2025-07-01-A1-Q2, E2025-07-01-A2-Q2, E2026-02-03-A3-Q1, E2026-02-03-A3-Q2
- `data:word-array-1000` - E2026-02-18-A1-Q1, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `data:word-array-10000-declared` - E2026-02-18-A2-Q1
- `data:writable-output` - E2023-02-07-Q1, E2025-01-29-A3-Q1

### Abi tags

- `abi:c-calls-assembly` - E2023-02-07-Q2, E2023-07-04-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `abi:c-calls-assembly-three-times` - E2025-01-29-A3-Q2
- `abi:callback` - E2024-02-28-Q2, E2024-09-16-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3
- `abi:callee-saved-registers` - E2023-02-07-Q1, E2023-02-24-Q1, E2023-02-24-Q2, E2023-05-17-Q1, E2023-07-04-Q1, E2023-09-18-Q1, E2024-02-12-Q1, E2024-02-28-Q1, E2024-07-09-Q1, E2024-09-16-Q1, E2025-01-29-A1-Q1, E2025-01-29-A2-Q1, E2025-01-29-A3-Q1, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1, E2025-07-01-A1-Q1, E2025-07-01-A2-Q1, E2026-02-03-A1-Q1, E2026-02-03-A2-Q1, E2026-02-03-A3-Q1, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1, E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- `abi:exception-return` - E2023-02-24-Q2
- `abi:five-arguments` - E2025-07-01-A1-Q1, E2025-07-01-A1-Q2, E2025-07-01-A2-Q1, E2025-07-01-A2-Q2
- `abi:flags-return-contract` - E2023-05-17-Q2
- `abi:four-register-arguments` - E2024-07-09-Q1, E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- `abi:non-leaf` - E2023-02-07-Q1, E2023-02-24-Q1, E2023-02-24-Q2, E2023-07-04-Q1, E2023-09-18-Q1, E2024-07-09-Q1, E2024-07-09-Q2, E2024-09-16-Q1, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1, E2025-07-01-A1-Q2, E2025-07-01-A2-Q2, E2026-02-03-A1-Q1, E2026-02-03-A3-Q1
- `abi:reset-handler` - E2024-07-09-Q2, E2025-07-01-A1-Q2, E2025-07-01-A2-Q2
- `abi:seven-arguments` - E2024-09-16-Q1
- `abi:stacked-argument` - E2025-07-01-A1-Q1, E2025-07-01-A2-Q1
- `abi:stacked-arguments` - E2024-09-16-Q1
- `abi:two-arguments` - E2026-02-18-A1-Q1, E2026-02-18-A2-Q1
- `abi:two-pointer-arguments` - E2025-01-29-A3-Q1
- `abi:two-register-wide-input` - E2023-05-17-Q1

### Risk tags

- `risk:adc-channel` - E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2
- `risk:arithmetic-overflow` - E2023-09-18-Q1
- `risk:bit-order` - E2025-01-29-A1-Q1, E2025-01-29-A2-Q1
- `risk:bounds` - E2023-02-07-Q1, E2024-02-12-Q1, E2024-02-12-Q2, E2024-02-28-Q1, E2024-07-09-Q1, E2024-09-16-Q1, E2025-01-29-A1-Q1, E2025-01-29-A2-Q1, E2025-01-29-A3-Q1, E2025-01-29-A3-Q2, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1, E2026-02-03-A1-Q1, E2026-02-03-A1-Q2, E2026-02-03-A2-Q1, E2026-02-03-A2-Q2, E2026-02-03-A3-Q1, E2026-02-03-A3-Q2, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1
- `risk:capacity` - E2026-02-03-A1-Q1, E2026-02-03-A2-Q1
- `risk:debounce` - E2023-02-07-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `risk:direct-register-setup` - E2024-07-09-Q2
- `risk:divide-by-zero` - E2023-05-17-Q1, E2025-07-01-A1-Q1
- `risk:division` - E2023-07-04-Q1
- `risk:duplicate-detection` - E2026-02-03-A3-Q1
- `risk:duplicates` - E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- `risk:event-order` - E2024-09-16-Q2
- `risk:final-run` - E2026-02-03-A1-Q1, E2026-02-03-A2-Q1
- `risk:first-event-latching` - E2025-07-01-A1-Q3, E2025-07-01-A2-Q3
- `risk:fixed-point-scale` - E2025-02-12-A1-Q1, E2025-02-12-A2-Q1
- `risk:indirect-index` - E2026-02-18-A1-Q1, E2026-02-18-A2-Q1
- `risk:irq-shared-state` - E2023-02-07-Q2, E2023-07-04-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-02-28-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `risk:large-static-array` - E2026-02-18-A2-Q1
- `risk:lost-events` - E2024-02-28-Q2
- `risk:msb-first-bit-order` - E2025-01-29-A3-Q1
- `risk:msp-vs-psp` - E2023-02-24-Q2
- `risk:no-progress-termination` - E2024-02-12-Q1
- `risk:non-returning-loop` - E2025-07-01-A1-Q2, E2025-07-01-A2-Q2
- `risk:nzcv-semantics` - E2023-05-17-Q2
- `risk:one-based-vs-zero-based` - E2026-02-18-A1-Q1, E2026-02-18-A2-Q1
- `risk:operator-precedence` - E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- `risk:overflow` - E2023-05-17-Q1, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1
- `risk:overflow-order` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `risk:positive-subtraction` - E2026-02-03-A3-Q1
- `risk:row-order` - E2025-01-29-A1-Q1
- `risk:running-state` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `risk:sample-bounds` - E2025-02-12-A1-Q2, E2025-02-12-A2-Q2
- `risk:sample-wrap` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `risk:secret-lifetime` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `risk:shift-range` - E2025-07-01-A2-Q1
- `risk:sign-normalization` - E2023-05-17-Q1
- `risk:signedness` - E2023-02-07-Q1, E2023-02-24-Q1, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1
- `risk:stack-alignment` - E2025-07-01-A1-Q2, E2025-07-01-A2-Q2
- `risk:stack-balance` - E2023-02-07-Q1, E2023-02-24-Q1, E2023-02-24-Q2, E2023-05-17-Q1, E2023-07-04-Q1, E2023-09-18-Q1, E2024-02-12-Q1, E2024-02-28-Q1, E2024-07-09-Q1, E2024-07-09-Q2, E2024-09-16-Q1, E2025-01-29-A1-Q1, E2025-01-29-A2-Q1, E2025-01-29-A3-Q1, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1, E2025-07-01-A1-Q1, E2025-07-01-A2-Q1, E2026-02-03-A1-Q1, E2026-02-03-A2-Q1, E2026-02-03-A3-Q1, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1, E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- `risk:stack-capacity` - E2024-07-09-Q1
- `risk:stacked-arguments` - E2025-07-01-A1-Q2, E2025-07-01-A2-Q2
- `risk:stacked-offset` - E2025-07-01-A1-Q1, E2025-07-01-A2-Q1
- `risk:stacked-offsets` - E2024-09-16-Q1
- `risk:state-transition` - E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `risk:svc-decode` - E2023-02-24-Q2
- `risk:termination` - E2023-02-24-Q1, E2023-07-04-Q1
- `risk:three-timer-ownership` - E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- `risk:timer-ownership` - E2023-02-07-Q2, E2023-07-04-Q2, E2024-02-12-Q2, E2024-02-28-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A3-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- `risk:unreachable-destination` - E2024-02-28-Q1
- `risk:unsigned-wrap` - E2025-07-01-A1-Q1, E2025-07-01-A2-Q1
- `risk:vector-ownership` - E2023-02-07-Q2, E2024-07-09-Q2
- `risk:zero-initialization` - E2026-06-25-B1-Q1, E2026-06-25-B2-Q1

## Machine-readable search

- `../04 - Reference/Atlas Data and Indexes/ARM_EXAM_ATLAS/indexes/question_search.csv`
- `../04 - Reference/Atlas Data and Indexes/ARM_EXAM_ATLAS/indexes/question_search.json`

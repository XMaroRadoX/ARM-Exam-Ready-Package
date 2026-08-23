# E2026-06-25-B1 - code start here

## E2026-06-25-B1-Q1

Implement BullsAndCows over four word arrays, count exact matches and frequency-based partial matches, and return the encoded result.

- `PAT-AAPCS-FOUR-ARGS-001`: [exam_asm.s](../../../../../Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/exam_asm.s) - Move long-lived R0-R3 pointers into preserved registers before reusing argument registers.
- `PAT-ALG-FREQUENCY-COUNT-001`: [exam_asm.s](../../../../../Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/exam_asm.s) - Choose frequency counters for a small value range or used markers for general values.
- `PAT-ADC-SAMPLE-001`: [adc_to_leds.c](../../../../CODE_TEMPLATES/03_board/adc_to_leds.c) - Normalize the 12-bit sample once, then pass the value to a small policy function.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-MEM-WORD-ARRAY-001`: [array_scan_word.s](../../../../CODE_TEMPLATES/02_algorithms/array_scan_word.s) - Use LSL #2 scaled addressing and pass element count, not byte count.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2026-06-25-B1-Q2

Build a debounced joystick-driven Bulls and Cows game, seed a four-digit secret from a free-running timer, show the guess and encoded result on LEDs, and retain the secret across guesses.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../CODE_TEMPLATES/03_board/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-GPIO-JOYSTICK-001`: [joystick_state_machine.c](../../../../CODE_TEMPLATES/03_board/joystick_state_machine.c) - Change the transition table and display policy, not the debounce/event plumbing.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-DEBOUNCE-001`: [button_debounce_event.c](../../../../CODE_TEMPLATES/03_board/button_debounce_event.c) - Change confirmation ticks in configuration; retain press and release edges.
- `PAT-STATE-EVENT-LOOP-001`: [joystick_state_machine.c](../../../../CODE_TEMPLATES/03_board/joystick_state_machine.c) - Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.
- `PAT-TIMER-FREE-RUNNING-001`: [free_running_timer.c](../../../../CODE_TEMPLATES/03_board/free_running_timer.c) - Use the counter as a seed/capture and do not enable the match interrupt unless required.
- `PAT-TIMER-PERIODIC-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Change the millisecond period and timer ID in the configuration call.


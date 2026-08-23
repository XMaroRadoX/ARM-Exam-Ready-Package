# E2026-02-18-A1 - code start here

## E2026-02-18-A1-Q1

Generate the iterative Hofstadter Q sequence in a word array and return or track the required maximum while handling early indices safely.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ALG-RECURRENCE-001`: [recurrence_into_array.s](../../../../CODE_TEMPLATES/02_algorithms/recurrence_into_array.s) - Change the seed block and the one recurrence-rule block; keep the array ABI.
- `PAT-MEM-WORD-ARRAY-001`: [array_scan_word.s](../../../../CODE_TEMPLATES/02_algorithms/array_scan_word.s) - Use LSL #2 scaled addressing and pass element count, not byte count.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.
- `PAT-TIMER-FREE-RUNNING-001`: [free_running_timer.c](../../../../CODE_TEMPLATES/03_board/free_running_timer.c) - Use the counter as a seed/capture and do not enable the match interrupt unless required.

## E2026-02-18-A1-Q2

Coordinate three timers for A/B/C states, stream SinTable[45] through the DAC, use a 50 ms scheduler tick, compute frequency/duration values, and track whether each timer is running.

- `PAT-ALG-FREQUENCY-COUNT-001`: [exam_asm.s](../../../../../Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/exam_asm.s) - Choose frequency counters for a small value range or used markers for general values.
- `PAT-ADC-SAMPLE-001`: [adc_to_leds.c](../../../../CODE_TEMPLATES/03_board/adc_to_leds.c) - Normalize the 12-bit sample once, then pass the value to a small policy function.
- `PAT-DAC-STREAM-001`: [dac_table_stream.c](../../../../CODE_TEMPLATES/03_board/dac_table_stream.c) - Change sample table and period; keep the ISR index bounded and wrap explicitly.
- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../CODE_TEMPLATES/03_board/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-TIMER-VECTOR-OWNERSHIP-001`: [multi_timer_state.c](../../../../CODE_TEMPLATES/03_board/multi_timer_state.c) - Select exactly one owner per IRQ handler and clear only that peripheral's pending source.
- `PAT-STATE-EVENT-LOOP-001`: [joystick_state_machine.c](../../../../CODE_TEMPLATES/03_board/joystick_state_machine.c) - Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.
- `PAT-TIMER-PERIODIC-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Change the millisecond period and timer ID in the configuration call.


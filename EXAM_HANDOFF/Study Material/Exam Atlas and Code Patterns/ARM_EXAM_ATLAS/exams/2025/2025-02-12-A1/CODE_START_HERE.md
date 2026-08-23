# E2025-02-12-A1 - code start here

## E2025-02-12-A1-Q1

Generate sine values with the stated Maclaurin/fixed-point recurrence, maintaining scale, signs, loop limits and array storage.

- `PAT-ALG-FIXED-POINT-001`: [fixed_point_recurrence.s](../../../../CODE_TEMPLATES/02_algorithms/fixed_point_recurrence.s) - Change Q format and coefficients; recalculate the post-SMULL shift.
- `PAT-ALG-RECURRENCE-001`: [recurrence_into_array.s](../../../../CODE_TEMPLATES/02_algorithms/recurrence_into_array.s) - Change the seed block and the one recurrence-rule block; keep the array ABI.
- `PAT-DAC-STREAM-001`: [dac_table_stream.c](../../../../CODE_TEMPLATES/03_board/dac_table_stream.c) - Change sample table and period; keep the ISR index bounded and wrap explicitly.
- `PAT-CPU-FLAGS-001`: [apsr_flags.s](../../../../CODE_TEMPLATES/04_rare_dangerous/apsr_flags.s) - Use the S-suffixed arithmetic instruction that naturally creates the required flags.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-MEM-WORD-ARRAY-001`: [array_scan_word.s](../../../../CODE_TEMPLATES/02_algorithms/array_scan_word.s) - Use LSL #2 scaled addressing and pass element count, not byte count.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2025-02-12-A1-Q2

On INT0, call the assembly generator for sineValues[45]; configure Timer0 every 1263 cycles and stream the samples to the DAC; no debouncing is required.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ADC-SAMPLE-001`: [adc_to_leds.c](../../../../CODE_TEMPLATES/03_board/adc_to_leds.c) - Normalize the 12-bit sample once, then pass the value to a small policy function.
- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../CODE_TEMPLATES/03_board/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-DEBOUNCE-001`: [button_debounce_event.c](../../../../CODE_TEMPLATES/03_board/button_debounce_event.c) - Change confirmation ticks in configuration; retain press and release edges.
- `PAT-TIMER-PERIODIC-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Change the millisecond period and timer ID in the configuration call.


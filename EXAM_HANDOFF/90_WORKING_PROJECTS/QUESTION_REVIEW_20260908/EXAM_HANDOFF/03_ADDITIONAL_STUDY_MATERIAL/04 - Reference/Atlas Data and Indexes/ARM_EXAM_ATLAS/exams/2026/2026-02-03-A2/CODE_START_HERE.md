# E2026-02-03-A2 - code start here

## E2026-02-03-A2-Q1

Run-length encode the digit array into the required count/value format, including final-run handling and output length.

- `PAT-FLOW-EARLY-BREAK-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Branch to one named inner-loop exit; do not bypass stack restoration.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.
- `PAT-MEM-WORD-ARRAY-001`: [array_scan_word.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/array_scan_word.s) - Use LSL #2 scaled addressing and pass element count, not byte count.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2026-02-03-A2-Q2

Read the potentiometer with ADC, show its high eight bits on LEDs, and invoke the encoder from KEY1 with the required debounce behavior.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ADC-SAMPLE-001`: [adc_to_leds.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/adc_to_leds.c) - Normalize the 12-bit sample once, then pass the value to a small policy function.
- `PAT-DAC-STREAM-001`: [dac_table_stream.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/dac_table_stream.c) - Change sample table and period; keep the ISR index bounded and wrap explicitly.
- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-DEBOUNCE-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Change confirmation ticks in configuration; retain press and release edges.


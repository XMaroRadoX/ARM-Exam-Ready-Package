# E2023-02-07 - code start here

## E2023-02-07-Q1

Copy signed byte values into a working array, then perform insertion sort while preserving signed ordering and array bounds.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ALG-SORTING-001`: [array_scan_word.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/array_scan_word.s) - Change element width/signed load, comparison condition, and length.
- `PAT-CPU-SVC-001`: [svc_handler.s](../../../../../../02%20-%20Code%20Recipes/07%20-%20Interrupts%20and%20Exceptions/svc_handler.s) - Decode the byte at stacked PC-2 and write return values into the stacked frame.
- `PAT-FLOW-EARLY-BREAK-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Branch to one named inner-loop exit; do not bypass stack restoration.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2023-02-07-Q2

Use Timer1 as a free-running counter reset at 0xFF without an IRQ; INT0 captures array data and alternates LEDs 6/7; KEY1 invokes the assembly sort.

- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-TIMER-VECTOR-OWNERSHIP-001`: [multi_timer_state.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/multi_timer_state.c) - Select exactly one owner per IRQ handler and clear only that peripheral's pending source.
- `PAT-STATE-DEBOUNCE-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Change confirmation ticks in configuration; retain press and release edges.
- `PAT-TIMER-FREE-RUNNING-001`: [free_running_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/free_running_timer.c) - Use the counter as a seed/capture and do not enable the match interrupt unless required.


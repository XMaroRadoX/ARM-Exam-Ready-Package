# E2025-01-29-A2 - code start here

## E2025-01-29-A2-Q1

Multiply two packed binary matrices using bit-level dot products and store the packed result with the required orientation.

- `PAT-FLOW-EARLY-BREAK-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Branch to one named inner-loop exit; do not bypass stack restoration.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2025-01-29-A2-Q2

Use the specified free-running timer and interrupts to fill matrices A and B; invoke multiplication on KEY1; display result rows on LEDs every 0.5 seconds.

- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-CPU-FLAGS-001`: [apsr_flags.s](../../../../../../02%20-%20Code%20Recipes/07%20-%20Interrupts%20and%20Exceptions/apsr_flags.s) - Use the S-suffixed arithmetic instruction that naturally creates the required flags.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-TIMER-FREE-RUNNING-001`: [free_running_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/free_running_timer.c) - Use the counter as a seed/capture and do not enable the match interrupt unless required.
- `PAT-TIMER-PERIODIC-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Change the millisecond period and timer ID in the configuration call.


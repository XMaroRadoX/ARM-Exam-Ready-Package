# E2024-02-12 - code start here

## E2024-02-12-Q1

Solve a two-dimensional byte maze by repeatedly propagating reachable distances until the destination is reached or no progress remains.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ALG-GRAPH-SEARCH-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Keep row-major addressing; replace only neighbor/edge acceptance and termination policy.
- `PAT-FLOW-EARLY-BREAK-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Branch to one named inner-loop exit; do not bypass stack restoration.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2024-02-12-Q2

Generate a random maze with an LCG seeded from a free-running Timer0, start from KEY2, fill the byte matrix safely, and call the assembly solver.

- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-CPU-FLAGS-001`: [apsr_flags.s](../../../../../../02%20-%20Code%20Recipes/07%20-%20Interrupts%20and%20Exceptions/apsr_flags.s) - Use the S-suffixed arithmetic instruction that naturally creates the required flags.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-DEBOUNCE-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Change confirmation ticks in configuration; retain press and release edges.
- `PAT-STATE-EVENT-LOOP-001`: [joystick_state_machine.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/joystick_state_machine.c) - Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.
- `PAT-TIMER-FREE-RUNNING-001`: [free_running_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/free_running_timer.c) - Use the counter as a seed/capture and do not enable the match interrupt unless required.


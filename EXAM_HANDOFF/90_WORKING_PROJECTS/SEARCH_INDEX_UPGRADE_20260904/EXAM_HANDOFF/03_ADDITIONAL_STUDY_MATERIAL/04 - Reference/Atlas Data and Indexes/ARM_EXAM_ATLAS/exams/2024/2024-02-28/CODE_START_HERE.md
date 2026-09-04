# E2024-02-28 - code start here

## E2024-02-28-Q1

Compute a shortest path through a two-dimensional byte maze while respecting walls, bounds and distance updates.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ALG-GRAPH-SEARCH-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Keep row-major addressing; replace only neighbor/edge acceptance and termination policy.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2024-02-28-Q2

Configure a timer for a 0.5-second sequence and move an LED indication through the required states without losing events.

- `PAT-ALG-RECURRENCE-001`: [recurrence_into_array.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/recurrence_into_array.s) - Change the seed block and the one recurrence-rule block; keep the array ABI.
- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-EVENT-LOOP-001`: [joystick_state_machine.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/joystick_state_machine.c) - Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.
- `PAT-TIMER-PERIODIC-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Change the millisecond period and timer ID in the configuration call.


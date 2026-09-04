# E2024-07-09 - code start here

## E2024-07-09-Q1

Solve a maze with depth-first search using an explicit stack, four parameters and a nested call to chooseNeighbor.

- `PAT-AAPCS-FOUR-ARGS-001`: [assembly.s](../../../../../../03%20-%20Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/assembly.s) - Move long-lived R0-R3 pointers into preserved registers before reusing argument registers.
- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ALG-GRAPH-SEARCH-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Keep row-major addressing; replace only neighbor/edge acceptance and termination policy.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2024-07-09-Q2

Configure SysTick directly in Reset_Handler, collect available moves, choose one using modulo arithmetic, and keep the stack balanced across all branches.

- `PAT-ALG-RECURRENCE-001`: [recurrence_into_array.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/recurrence_into_array.s) - Change the seed block and the one recurrence-rule block; keep the array ABI.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-TIMER-PERIODIC-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Change the millisecond period and timer ID in the configuration call.


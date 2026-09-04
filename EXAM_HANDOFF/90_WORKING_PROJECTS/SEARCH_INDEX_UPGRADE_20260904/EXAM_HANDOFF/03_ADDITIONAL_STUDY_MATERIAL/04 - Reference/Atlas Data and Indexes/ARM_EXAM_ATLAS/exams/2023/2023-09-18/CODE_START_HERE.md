# E2023-09-18 - code start here

## E2023-09-18-Q1

Implement digitSum and digitaddition so one assembly subroutine calls another and reports arithmetic overflow correctly.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-CPU-FLAGS-001`: [apsr_flags.s](../../../../../../02%20-%20Code%20Recipes/07%20-%20Interrupts%20and%20Exceptions/apsr_flags.s) - Use the S-suffixed arithmetic instruction that naturally creates the required flags.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2023-09-18-Q2

Use KEY1 and KEY2 to build a binary value K, trigger processing from INT0, manage arrays, call assembly and show the comparison result on LEDs.

- `PAT-ALG-RECURRENCE-001`: [recurrence_into_array.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/recurrence_into_array.s) - Change the seed block and the one recurrence-rule block; keep the array ABI.
- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-DEBOUNCE-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Change confirmation ticks in configuration; retain press and release edges.
- `PAT-STATE-EVENT-LOOP-001`: [joystick_state_machine.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/joystick_state_machine.c) - Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.


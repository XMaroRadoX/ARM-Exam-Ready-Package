# E2024-09-16 - code start here

## E2024-09-16-Q1

Implement the Kruskal-style maze operation across three arrays with seven parameters, including min/max selection, component replacement and row-major access.

- `PAT-AAPCS-FOUR-ARGS-001`: [exam_asm.s](../../../../../Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/exam_asm.s) - Move long-lived R0-R3 pointers into preserved registers before reusing argument registers.
- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-AAPCS-STACKED-ARGS-001`: [five_to_seven_arguments.s](../../../../CODE_TEMPLATES/01_aapcs/five_to_seven_arguments.s) - Capture the caller's original SP before PUSH and calculate offsets from that value.
- `PAT-ALG-GRAPH-SEARCH-001`: [matrix_row_major_byte.s](../../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s) - Keep row-major addressing; replace only neighbor/edge acceptance and termination policy.
- `PAT-CPU-FLAGS-001`: [apsr_flags.s](../../../../CODE_TEMPLATES/04_rare_dangerous/apsr_flags.s) - Use the S-suffixed arithmetic instruction that naturally creates the required flags.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../CODE_TEMPLATES/02_algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2024-09-16-Q2

Implement a two-button state machine that increments a value and applies the required offset while handling event order and button behavior.

- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../CODE_TEMPLATES/03_board/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../CODE_TEMPLATES/03_board/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-DEBOUNCE-001`: [button_debounce_event.c](../../../../CODE_TEMPLATES/03_board/button_debounce_event.c) - Change confirmation ticks in configuration; retain press and release edges.
- `PAT-STATE-EVENT-LOOP-001`: [joystick_state_machine.c](../../../../CODE_TEMPLATES/03_board/joystick_state_machine.c) - Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.


# E2025-07-01-A2 - code start here

## E2025-07-01-A2-Q1

Implement the variant LCG with its shift operation and five-argument interface, preserving the specified arithmetic order.

- `PAT-AAPCS-STACKED-ARGS-001`: [five_to_seven_arguments.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/five_to_seven_arguments.s) - Capture the caller's original SP before PUSH and calculate offsets from that value.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2025-07-01-A2-Q2

Drive the variant generator from Reset_Handler with correct argument construction and persistent loop state.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ALG-RECURRENCE-001`: [recurrence_into_array.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/recurrence_into_array.s) - Change the seed block and the one recurrence-rule block; keep the array ABI.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-WORD-ARRAY-001`: [array_scan_word.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/array_scan_word.s) - Use LSL #2 scaled addressing and pass element count, not byte count.

## E2025-07-01-A2-Q3

Use Timer1 for a 2.5-second LED sequence and process only the joystick's first movement in the game logic.

- `PAT-GPIO-EVENT-001`: [button_debounce_event.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/button_debounce_event.c) - Publish an event in the callback and consume it once in foreground.
- `PAT-GPIO-JOYSTICK-001`: [joystick_state_machine.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/joystick_state_machine.c) - Change the transition table and display policy, not the debounce/event plumbing.
- `PAT-TIMER-OWNERSHIP-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Assign each timer/vector once and keep the callback bounded.
- `PAT-STATE-IRQ-HANDOFF-001`: [periodic_timer.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c) - Make shared events volatile/atomic through the kit API and take them once in foreground.
- `PAT-STATE-EVENT-LOOP-001`: [joystick_state_machine.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/joystick_state_machine.c) - Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.


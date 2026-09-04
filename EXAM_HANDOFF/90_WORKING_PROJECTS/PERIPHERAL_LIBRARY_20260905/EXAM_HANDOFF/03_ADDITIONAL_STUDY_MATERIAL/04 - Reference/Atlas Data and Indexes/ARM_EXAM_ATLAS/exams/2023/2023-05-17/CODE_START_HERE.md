# E2023-05-17 - code start here

## E2023-05-17-Q1

Divide a signed 64-bit dividend by a signed 32-bit divisor without MUL, using sign normalization, a 64-bit shift/subtract loop, and quotient-bit construction.

- `PAT-ADC-SAMPLE-001`: [adc_to_leds.c](../../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/adc_to_leds.c) - Normalize the 12-bit sample once, then pass the value to a small policy function.
- `PAT-CPU-FLAGS-001`: [apsr_flags.s](../../../../../../02%20-%20Code%20Recipes/07%20-%20Interrupts%20and%20Exceptions/apsr_flags.s) - Use the S-suffixed arithmetic instruction that naturally creates the required flags.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../../../02%20-%20Code%20Recipes/04%20-%20Algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2023-05-17-Q2

Set or report the required N, Z, C and V status according to the division outcome using program-status-register operations.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.


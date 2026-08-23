# E2023-02-24 - code start here

## E2023-02-24-Q1

Implement the Kaprekar digit transformation, including digit extraction, reordering, subtraction and repeated convergence logic.

- `PAT-AAPCS-NONLEAF-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Save LR before the first BL and save an even total number of registers.
- `PAT-ALG-RECURRENCE-001`: [recurrence_into_array.s](../../../../CODE_TEMPLATES/02_algorithms/recurrence_into_array.s) - Change the seed block and the one recurrence-rule block; keep the array ABI.
- `PAT-ALG-SORTING-001`: [array_scan_word.s](../../../../CODE_TEMPLATES/02_algorithms/array_scan_word.s) - Change element width/signed load, comparison condition, and length.
- `PAT-FLOW-NESTED-LOOP-001`: [nested_search_with_break.s](../../../../CODE_TEMPLATES/02_algorithms/nested_search_with_break.s) - Keep outer state in preserved registers and reset the inner index at each outer iteration.
- `PAT-MEM-MATRIX-ROW-MAJOR-001`: [matrix_row_major_byte.s](../../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s) - Compute row * columns + column, then apply the element-size or packed-bit transform.
- `PAT-AAPCS-STACK-SAFETY-001`: [nonleaf_function.s](../../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s) - Preserve R4-R11, save LR before BL, and push an even register count.

## E2023-02-24-Q2

Handle SVC #50, locate the correct exception stack frame, decode the SVC immediate from the instruction before stacked PC, repeatedly call the Kaprekar routine, and return the iteration count in R6.

- `PAT-CPU-EXCEPTION-FRAME-001`: [svc_handler.s](../../../../CODE_TEMPLATES/04_rare_dangerous/svc_handler.s) - Test EXC_RETURN bit 2 before selecting MSP or PSP; preserve EXC_RETURN in LR.
- `PAT-CPU-SVC-001`: [svc_handler.s](../../../../CODE_TEMPLATES/04_rare_dangerous/svc_handler.s) - Decode the byte at stacked PC-2 and write return values into the stacked frame.
- `PAT-MEM-BYTE-ARRAY-001`: [matrix_row_major_byte.s](../../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s) - Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.


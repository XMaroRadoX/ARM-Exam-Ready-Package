# Exam mapping

- Exam ID: `E2023-02-24`
- Questions: `E2023-02-24-Q1`, `E2023-02-24-Q2`
- Tags: `abi:nonleaf`, `alg:recurrence`, `alg:sorting`, `cpu:exception-frame`, `cpu:svc`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-SORTING-001`, `PAT-CPU-EXCEPTION-FRAME-001`, `PAT-CPU-SVC-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2023-02-24-Q1` | Implement the Kaprekar digit transformation, including digit extraction, reordering, subtraction and repeated convergence logic. | `Material (8)\Exams\22-23\20230224 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2023-02-24-Q2` | Handle SVC #50, locate the correct exception stack frame, decode the SVC immediate from the instruction before stacked PC, repeatedly call the Kaprekar routine, and return the iteration count in R6. | `Material (8)\Exams\22-23\20230224 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

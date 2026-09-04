# E2023-02-24-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:recurrence`, `alg:sorting`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-SORTING-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\22-23\20230224 arm.pdf`

## Requirement

Implement the Kaprekar digit transformation, including digit extraction, reordering, subtraction and repeated convergence logic.

## Concepts

decimal digits; division/remainder; sorting a small set; recurrence loop

## Constraints and risks

N/A; Nested helper calls require LR protection and callee-saved discipline.

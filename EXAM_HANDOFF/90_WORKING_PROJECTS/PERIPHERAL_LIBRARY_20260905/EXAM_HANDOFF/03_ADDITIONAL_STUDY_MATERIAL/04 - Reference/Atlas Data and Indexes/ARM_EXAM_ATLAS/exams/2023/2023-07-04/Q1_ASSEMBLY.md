# E2023-07-04-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:recurrence`, `flow:nested-loop`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\22-23\20230704 arm.pdf`

## Requirement

Compute aliquot sums and detect a sociable-number sequence using divisor tests, nested loops and subroutine calls.

## Concepts

proper divisors; modulo; recurrence; cycle detection; nested calls

## Constraints and risks

N/A; Nested BL calls must preserve LR; loop state belongs in callee-saved registers or stack slots.

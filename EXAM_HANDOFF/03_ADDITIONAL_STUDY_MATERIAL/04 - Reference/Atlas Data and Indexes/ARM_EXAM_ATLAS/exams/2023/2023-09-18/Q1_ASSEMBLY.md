# E2023-09-18-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `cpu:flags`, `flow:nested-loop`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\22-23\20230918 arm.pdf`

## Requirement

Implement digitSum and digitaddition so one assembly subroutine calls another and reports arithmetic overflow correctly.

## Concepts

decimal digits; nested subroutines; accumulation; overflow detection

## Constraints and risks

N/A; Save LR before nested BL; preserve R4-R11; return values and status must be defined.

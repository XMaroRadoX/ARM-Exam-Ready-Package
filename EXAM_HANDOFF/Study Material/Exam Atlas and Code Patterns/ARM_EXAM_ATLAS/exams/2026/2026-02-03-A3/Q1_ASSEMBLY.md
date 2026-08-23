# E2026-02-03-A3-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:recurrence`, `flow:nested-loop`, `mem:word-array`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material 2026\Exams\20260203_ARM_3.pdf`

## Requirement

Fill a word array with the Recaman sequence, selecting subtraction only when positive and not already present, otherwise addition.

## Concepts

recurrence; word array; linear search for duplicates; signed/unsigned decision; nested loop

## Constraints and risks

N/A; Pointer/length input and returned count/status; preserve outer index during duplicate-search helper.

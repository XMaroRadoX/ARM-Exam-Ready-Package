# E2026-02-18-A2-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:recurrence`, `mem:matrix-row-major`, `mem:word-array`, `risk:stack-alignment`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-TIMER-FREE-RUNNING-001`
- Source: `Material 2026\Exams\20260218_ARM_2.pdf`

## Requirement

Generate the Hofstadter-Conway variant iteratively in a word array with correct seeds, recurrence-derived indexes and requested aggregate/result.

## Concepts

self-indexed recurrence; word array; seed cases; bounds; aggregate tracking

## Constraints and risks

N/A; Define array/length/result and protect derived indexes from underflow/out-of-range access.

# E2026-02-18-A1-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:recurrence`, `mem:word-array`, `risk:stack-alignment`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-TIMER-FREE-RUNNING-001`
- Source: `Material 2026\Exams\20260218_ARM_1.pdf`

## Requirement

Generate the iterative Hofstadter Q sequence in a word array and return or track the required maximum while handling early indices safely.

## Concepts

self-indexed recurrence; word array; maximum tracking; bounds/index validation

## Constraints and risks

N/A; Array pointer/length and max return value; validate recurrence-derived indexes before loads.

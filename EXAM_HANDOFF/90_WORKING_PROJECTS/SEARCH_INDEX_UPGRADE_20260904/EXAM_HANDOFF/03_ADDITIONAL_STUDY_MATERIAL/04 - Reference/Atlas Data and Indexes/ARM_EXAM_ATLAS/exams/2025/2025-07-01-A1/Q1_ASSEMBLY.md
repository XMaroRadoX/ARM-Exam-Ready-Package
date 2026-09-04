# E2025-07-01-A1-Q1

- Delivery: `ASM`
- Tags: `abi:stacked-args`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-STACKED-ARGS-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\24-25\2025_07_01\ARM1.pdf`

## Requirement

Implement the requested linear congruential generator with five parameters and correct unsigned wraparound/modulo behavior.

## Concepts

LCG; five arguments; stacked fifth argument; multiply/add/modulo

## Constraints and risks

N/A; Load argument 5 from the caller stack using the offset after any prologue; preserve R4-R11 and align SP.

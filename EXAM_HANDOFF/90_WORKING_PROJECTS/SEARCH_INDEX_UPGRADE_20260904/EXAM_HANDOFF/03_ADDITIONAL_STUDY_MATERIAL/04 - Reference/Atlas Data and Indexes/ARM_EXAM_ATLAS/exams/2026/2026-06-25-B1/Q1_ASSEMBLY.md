# E2026-06-25-B1-Q1

- Delivery: `ASM`
- Tags: `abi:four-register-args`, `alg:frequency-count`, `board:adc`, `mem:matrix-row-major`, `mem:word-array`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ADC-SAMPLE-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Exams\Exam 25.06.2206\20260625_ARM_1.pdf`

## Requirement

Implement BullsAndCows over four word arrays, count exact matches and frequency-based partial matches, and return the encoded result.

## Concepts

four arrays; two passes; frequency counting; min selection; encoded return

## Constraints and risks

N/A; Four pointers consume R0-R3; preserve R4-R11; frequency indexes are constrained to 0-3; restore SP exactly.

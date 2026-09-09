# E2025-01-29-A3-Q1

- Delivery: `ASM`
- Tags: `board:dac`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-DAC-STREAM-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM3.pdf`

## Requirement

Transpose a packed binary matrix by exchanging row/column bit coordinates without corrupting unrelated bits.

## Concepts

packed-bit transpose; get/set bit; nested loops; separate or in-place output

## Constraints and risks

N/A; Document input/output aliasing and packed layout.

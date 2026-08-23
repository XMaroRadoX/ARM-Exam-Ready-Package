# E2025-01-29-A1-Q1

- Delivery: `ASM`
- Tags: `alg:fixed-point`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-ALG-FIXED-POINT-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM1.pdf`

## Requirement

Apply the requested bitwise affine transformation to a packed 8x8 binary matrix while preserving the specified bit and row order.

## Concepts

packed 8x8 bits; row/column mapping; XOR/AND/OR; looped bit extraction and insertion

## Constraints and risks

N/A; Pointer and output contract must state byte order and whether in-place update is allowed.

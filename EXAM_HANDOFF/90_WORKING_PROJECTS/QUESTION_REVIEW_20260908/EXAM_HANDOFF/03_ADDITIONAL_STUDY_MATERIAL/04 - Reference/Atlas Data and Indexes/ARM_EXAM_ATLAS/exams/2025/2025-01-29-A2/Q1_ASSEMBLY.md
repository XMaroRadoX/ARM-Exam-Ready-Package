# E2025-01-29-A2-Q1

- Delivery: `ASM`
- Tags: `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM2.pdf`

## Requirement

Multiply two packed binary matrices using bit-level dot products and store the packed result with the required orientation.

## Concepts

packed-bit matrices; triple nested loops; Boolean dot product; bit packing

## Constraints and risks

N/A; Three matrix pointers and dimensions must fit the chosen interface without clobbering live loop state.

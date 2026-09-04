# PAT-MEM-MATRIX-ROW-MAJOR-001: Row-major matrix addressing

- Recognition tag: `mem:matrix-row-major`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-24`, `E2023-05-17`, `E2023-09-18`, `E2024-02-12`, `E2024-02-28`, `E2024-07-09`, `E2024-09-16`, `E2025-01-29-A1`, `E2025-01-29-A2`, `E2025-01-29-A3`, `E2025-02-12-A1`, `E2026-02-18-A2`, `E2026-06-25-B1`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`matrix_row_major_byte.s`](../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s)
- Alternative: [`packed_bit_matrix.s`](../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/packed_bit_matrix.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Compute row * columns + column, then apply the element-size or packed-bit transform.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

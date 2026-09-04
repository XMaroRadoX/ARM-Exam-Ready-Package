# PAT-MEM-BYTE-ARRAY-001: Signed and unsigned byte arrays

- Recognition tag: `mem:byte-array`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-07`, `E2023-02-24`, `E2024-02-12`, `E2024-02-28`, `E2024-07-09`, `E2024-09-16`, `E2025-01-29-A1`, `E2025-01-29-A2`, `E2025-01-29-A3`, `E2026-02-03-A1`, `E2026-02-03-A2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`matrix_row_major_byte.s`](../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/matrix_row_major_byte.s)
- Alternative: [`array_scan_word.s`](../../../../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/array_scan_word.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Use LDRB for unsigned bytes or LDRSB for signed bytes; index scale is one.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

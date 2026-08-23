# PAT-ALG-GRAPH-SEARCH-001: Matrix and graph traversal

- Recognition tag: `alg:graph-search`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2024-02-12`, `E2024-02-28`, `E2024-07-09`, `E2024-09-16`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`matrix_row_major_byte.s`](../../../CODE_TEMPLATES/02_algorithms/matrix_row_major_byte.s)
- Alternative: [`exam_asm.s`](../../../../Solved%20Exams/2025-01-29_ARM2_Matrix_Two_Timers/Answer%20Source/exam_asm.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Keep row-major addressing; replace only neighbor/edge acceptance and termination policy.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

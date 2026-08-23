# PAT-ALG-FIXED-POINT-001: Fixed-point multiply and recurrence

- Recognition tag: `alg:fixed-point`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2025-01-29-A1`, `E2025-02-12-A1`, `E2025-02-12-A2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`fixed_point_recurrence.s`](../../../CODE_TEMPLATES/02_algorithms/fixed_point_recurrence.s)
- Alternative: [`exam_asm.s`](../../../../Solved%20Exams/2025-02-12_ARM1_Sine_DAC/Answer%20Source/exam_asm.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Change Q format and coefficients; recalculate the post-SMULL shift.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

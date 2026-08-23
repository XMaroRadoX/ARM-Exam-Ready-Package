# PAT-ALG-FREQUENCY-COUNT-001: Frequency-count comparison

- Recognition tag: `alg:frequency-count`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2026-02-18-A1`, `E2026-02-18-A2`, `E2026-06-25-B1`, `E2026-06-25-B2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`exam_asm.s`](../../../../Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/exam_asm.s)
- Alternative: [`exam_asm.s`](../../../../Solved%20Exams/2026-06-25_ARM2_Mastermind/Answer%20Source/exam_asm.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Choose frequency counters for a small value range or used markers for general values.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

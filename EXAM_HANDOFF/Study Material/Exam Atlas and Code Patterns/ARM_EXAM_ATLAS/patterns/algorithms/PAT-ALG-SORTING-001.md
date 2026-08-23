# PAT-ALG-SORTING-001: Signed and unsigned array sorting

- Recognition tag: `alg:sorting`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-07`, `E2023-02-24`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`array_scan_word.s`](../../../CODE_TEMPLATES/02_algorithms/array_scan_word.s)
- Alternative: [`exam_asm.s`](../../../../Solved%20Exams/2023-02-07_Sort_FreeRunning_Timer/Answer%20Source/exam_asm.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Change element width/signed load, comparison condition, and length.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

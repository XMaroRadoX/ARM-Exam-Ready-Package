# PAT-ALG-RECURRENCE-001: Bounded recurrence into an array

- Recognition tag: `alg:recurrence`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-24`, `E2023-07-04`, `E2023-09-18`, `E2024-02-28`, `E2024-07-09`, `E2025-02-12-A1`, `E2025-02-12-A2`, `E2025-07-01-A1`, `E2025-07-01-A2`, `E2026-02-03-A1`, `E2026-02-03-A3`, `E2026-02-18-A1`, `E2026-02-18-A2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`recurrence_into_array.s`](../../../CODE_TEMPLATES/02_algorithms/recurrence_into_array.s)
- Alternative: [`exam_asm.s`](../../../../Solved%20Exams/2026-02-03_ARM3_Recaman_ADC_Timer/Answer%20Source/exam_asm.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Change the seed block and the one recurrence-rule block; keep the array ABI.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

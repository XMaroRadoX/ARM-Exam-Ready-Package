# PAT-FLOW-EARLY-BREAK-001: Balanced early exit from inner search

- Recognition tag: `flow:early-break`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-07`, `E2024-02-12`, `E2025-01-29-A2`, `E2026-02-03-A2`, `E2026-06-25-B2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`nested_search_with_break.s`](../../../CODE_TEMPLATES/02_algorithms/nested_search_with_break.s)
- Alternative: [`exam_asm.s`](../../../../Solved%20Exams/2026-06-25_ARM2_Mastermind/Answer%20Source/exam_asm.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Branch to one named inner-loop exit; do not bypass stack restoration.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

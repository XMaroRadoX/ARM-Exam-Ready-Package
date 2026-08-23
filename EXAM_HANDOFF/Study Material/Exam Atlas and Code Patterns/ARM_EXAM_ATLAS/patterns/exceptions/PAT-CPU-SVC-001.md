# PAT-CPU-SVC-001: SVC immediate decoding

- Recognition tag: `cpu:svc`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-07`, `E2023-02-24`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`svc_handler.s`](../../../CODE_TEMPLATES/04_rare_dangerous/svc_handler.s)
- Alternative: [`reset_handler.s`](../../../CODE_TEMPLATES/04_rare_dangerous/reset_handler.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Decode the byte at stacked PC-2 and write return values into the stacked frame.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

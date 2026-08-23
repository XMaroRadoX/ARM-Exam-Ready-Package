# PAT-CPU-FLAGS-001: APSR flag contract

- Recognition tag: `cpu:flags`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-05-17`, `E2023-09-18`, `E2024-02-12`, `E2024-09-16`, `E2025-01-29-A2`, `E2025-02-12-A1`, `E2025-07-01-A1`, `E2026-02-03-A1`, `E2026-02-03-A3`, `E2026-02-18-A2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`apsr_flags.s`](../../../CODE_TEMPLATES/04_rare_dangerous/apsr_flags.s)
- Alternative: [`two_word_arithmetic.s`](../../../CODE_TEMPLATES/04_rare_dangerous/two_word_arithmetic.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Use the S-suffixed arithmetic instruction that naturally creates the required flags.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

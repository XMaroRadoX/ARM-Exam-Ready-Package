# PAT-AAPCS-STACKED-ARGS-001: Fifth and later arguments

- Recognition tag: `abi:stacked-args`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2024-09-16`, `E2025-07-01-A1`, `E2025-07-01-A2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`five_to_seven_arguments.s`](../../../CODE_TEMPLATES/01_aapcs/five_to_seven_arguments.s)
- Alternative: [`nonleaf_function.s`](../../../CODE_TEMPLATES/01_aapcs/nonleaf_function.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Capture the caller's original SP before PUSH and calculate offsets from that value.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

# PAT-STATE-DEBOUNCE-001: Deterministic debounce

- Recognition tag: `state:debounce`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-07`, `E2023-09-18`, `E2024-02-12`, `E2024-09-16`, `E2025-01-29-A3`, `E2025-02-12-A1`, `E2026-02-03-A1`, `E2026-02-03-A2`, `E2026-06-25-B1`, `E2026-06-25-B2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`button_debounce_event.c`](../../../CODE_TEMPLATES/03_board/button_debounce_event.c)
- Alternative: [`joystick_state_machine.c`](../../../CODE_TEMPLATES/03_board/joystick_state_machine.c)
- Code status: `COMPILED_CODE`

## Change these lines first

Change confirmation ticks in configuration; retain press and release edges.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

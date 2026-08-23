# PAT-GPIO-JOYSTICK-001: Joystick event state machine

- Recognition tag: `board:joystick`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2025-07-01-A1`, `E2025-07-01-A2`, `E2026-06-25-B1`, `E2026-06-25-B2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`joystick_state_machine.c`](../../../CODE_TEMPLATES/03_board/joystick_state_machine.c)
- Alternative: [`button_debounce_event.c`](../../../CODE_TEMPLATES/03_board/button_debounce_event.c)
- Code status: `COMPILED_CODE`

## Change these lines first

Change the transition table and display policy, not the debounce/event plumbing.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

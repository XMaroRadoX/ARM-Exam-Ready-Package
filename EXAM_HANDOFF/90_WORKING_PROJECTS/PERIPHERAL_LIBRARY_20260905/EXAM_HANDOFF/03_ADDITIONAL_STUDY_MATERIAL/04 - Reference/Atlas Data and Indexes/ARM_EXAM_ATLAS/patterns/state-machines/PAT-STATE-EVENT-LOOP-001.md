# PAT-STATE-EVENT-LOOP-001: ISR-to-foreground event loop

- Recognition tag: `state:event-loop`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-07-04`, `E2023-09-18`, `E2024-02-12`, `E2024-02-28`, `E2024-09-16`, `E2025-01-29-A3`, `E2025-07-01-A1`, `E2025-07-01-A2`, `E2026-02-03-A1`, `E2026-02-03-A3`, `E2026-02-18-A1`, `E2026-02-18-A2`, `E2026-06-25-B1`, `E2026-06-25-B2`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`joystick_state_machine.c`](../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/joystick_state_machine.c)
- Alternative: [`periodic_timer.c`](../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/periodic_timer.c)
- Code status: `COMPILED_CODE`

## Change these lines first

Callbacks only set bits/data; the foreground loop owns algorithm calls and display changes.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

# PAT-ADC-SAMPLE-001: ADC sample conversion

- Recognition tag: `board:adc`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-05-17`, `E2025-02-12-A1`, `E2025-02-12-A2`, `E2026-02-03-A1`, `E2026-02-03-A2`, `E2026-02-03-A3`, `E2026-02-18-A1`, `E2026-02-18-A2`, `E2026-06-25-B1`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`adc_to_leds.c`](../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/adc_to_leds.c)
- Alternative: [`joystick_state_machine.c`](../../../../../02%20-%20Code%20Recipes/08%20-%20Board%20Components/joystick_state_machine.c)
- Code status: `COMPILED_CODE`

## Change these lines first

Normalize the 12-bit sample once, then pass the value to a small policy function.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

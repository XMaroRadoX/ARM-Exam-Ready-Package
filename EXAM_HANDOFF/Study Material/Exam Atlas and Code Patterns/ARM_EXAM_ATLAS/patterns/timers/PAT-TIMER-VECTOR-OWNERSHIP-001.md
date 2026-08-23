# PAT-TIMER-VECTOR-OWNERSHIP-001: Exclusive interrupt-vector ownership

- Recognition tag: `risk:vector-ownership`
- Input/output contract: use the linked exam routine's documented AAPCS prototype.
- Registers: R0-R3 and flags are caller-clobbered; preserve R4-R11.
- Stack: restore SP exactly and keep eight-byte alignment at public call boundaries.
- Signedness/width: select explicit LDRB/LDRSB/LDRH/LDRSH/LDR according to the paper.
- Adaptation: change constants or the localized rule block before changing the ABI.
- Common failures: wrong signed branch, unbalanced early exit, overwritten LR, or unchecked bounds.
- Related exams: `E2023-02-07`, `E2026-02-18-A1`
- Tests: each related project `Tests/` and `Reports/COVERAGE_MATRIX.csv`.


## Start with actual code

- Canonical: [`multi_timer_state.c`](../../../CODE_TEMPLATES/03_board/multi_timer_state.c)
- Alternative: [`systick_raw.s`](../../../CODE_TEMPLATES/04_rare_dangerous/systick_raw.s)
- Code status: `COMPILED_CODE`

## Change these lines first

Select exactly one owner per IRQ handler and clear only that peripheral's pending source.

The linked source is the pattern. This page is navigation and adaptation guidance, not a substitute for the code.

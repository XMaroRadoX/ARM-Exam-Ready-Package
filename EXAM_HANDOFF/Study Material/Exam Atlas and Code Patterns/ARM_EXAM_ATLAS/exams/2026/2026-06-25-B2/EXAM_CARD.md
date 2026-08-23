# E2026-06-25-B2

- Date: `2026-06-25`
- Variant: `ARM2`
- Source PDF: `Exams/Exam 25.06.2206/20260625_ARM_2.pdf`
- SHA-256: `b643106147d4a20efe44ea7d6d39f1ec8dfc44d76d1625114779893efacb7124`
- Answer collection: `Study Material/Solved Exams/2026-06-25_ARM1_BullsAndCows`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `alg:frequency-count`, `board:gpio`, `board:joystick`, `board:timer`, `flow:early-break`, `flow:nested-loop`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2026-06-25-B1`, `E2026-02-18-A1`, `E2025-01-29-A3`, `E2024-02-12`, `E2026-02-18-A2`

## Questions

### Q1 - ASM

Implement Mastermind over four word arrays, mark exact matches, find unmatched partial matches with a nested search and break, and return the encoded result.

**Traps:** Four pointers consume R0-R3; preserve outer-loop state and R4-R11; every early break must keep SP balanced.

### Q2 - C + ASM call

Build the corresponding debounced joystick-driven Mastermind game with timer-derived secret, per-digit LED fields, repeated guesses and encoded result display.

**Traps:** Callbacks capture events only; clear used arrays before every call; retain the secret between attempts.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

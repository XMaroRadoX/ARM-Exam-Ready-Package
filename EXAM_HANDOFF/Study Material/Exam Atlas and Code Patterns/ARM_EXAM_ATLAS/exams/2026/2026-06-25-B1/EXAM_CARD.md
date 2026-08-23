# E2026-06-25-B1

- Date: `2026-06-25`
- Variant: `ARM1`
- Source PDF: `Exams/Exam 25.06.2206/20260625_ARM_1.pdf`
- SHA-256: `a3f7eaca07f96a281382237948255abc1fadcfd2a3502d2e4d604921128fa2a8`
- Answer collection: `Study Material/Solved Exams/2026-06-25_ARM1_BullsAndCows`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `alg:frequency-count`, `board:adc`, `board:gpio`, `board:joystick`, `board:timer`, `mem:matrix-row-major`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2026-06-25-B2`, `E2026-02-18-A2`, `E2026-02-18-A1`, `E2025-02-12-A1`, `E2025-01-29-A3`

## Questions

### Q1 - ASM

Implement BullsAndCows over four word arrays, count exact matches and frequency-based partial matches, and return the encoded result.

**Traps:** Four pointers consume R0-R3; preserve R4-R11; frequency indexes are constrained to 0-3; restore SP exactly.

### Q2 - C + ASM call

Build a debounced joystick-driven Bulls and Cows game, seed a four-digit secret from a free-running timer, show the guess and encoded result on LEDs, and retain the secret across guesses.

**Traps:** Callbacks capture events only; clear frequency arrays before every call; do not change the secret between guesses.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

# Exam mapping

- Exam ID: `E2026-06-25-B1`
- Questions: `E2026-06-25-B1-Q1`, `E2026-06-25-B1-Q2`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `alg:frequency-count`, `board:adc`, `board:gpio`, `board:joystick`, `board:timer`, `mem:matrix-row-major`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2026-06-25-B1-Q1` | Implement BullsAndCows over four word arrays, count exact matches and frequency-based partial matches, and return the encoded result. | `Exams\Exam 25.06.2206\20260625_ARM_1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2026-06-25-B1-Q2` | Build a debounced joystick-driven Bulls and Cows game, seed a four-digit secret from a free-running timer, show the guess and encoded result on LEDs, and retain the secret across guesses. | `Exams\Exam 25.06.2206\20260625_ARM_1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

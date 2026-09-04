# Exam mapping

- Exam ID: `E2026-06-25-B2`
- Questions: `E2026-06-25-B2-Q1`, `E2026-06-25-B2-Q2`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `alg:frequency-count`, `board:gpio`, `board:joystick`, `board:timer`, `flow:early-break`, `flow:nested-loop`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2026-06-25-B2-Q1` | Implement Mastermind over four word arrays, mark exact matches, find unmatched partial matches with a nested search and break, and return the encoded result. | `Exams\Exam 25.06.2206\20260625_ARM_2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2026-06-25-B2-Q2` | Build the corresponding debounced joystick-driven Mastermind game with timer-derived secret, per-digit LED fields, repeated guesses and encoded result display. | `Exams\Exam 25.06.2206\20260625_ARM_2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

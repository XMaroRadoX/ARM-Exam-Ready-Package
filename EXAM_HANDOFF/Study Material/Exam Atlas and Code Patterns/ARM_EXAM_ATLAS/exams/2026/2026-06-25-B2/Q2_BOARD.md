# E2026-06-25-B2-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `board:gpio`, `board:joystick`, `board:timer`, `risk:irq-shared-state`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Exams\Exam 25.06.2206\20260625_ARM_2.pdf`

## Requirement

Build the corresponding debounced joystick-driven Mastermind game with timer-derived secret, per-digit LED fields, repeated guesses and encoded result display.

## Concepts

foreground state machine; timer seed; nibble extraction; two-bit LED fields; debounced joystick events

## Constraints and risks

Physical debounce required; secret captured only once per game; Callbacks capture events only; clear used arrays before every call; retain the secret between attempts.

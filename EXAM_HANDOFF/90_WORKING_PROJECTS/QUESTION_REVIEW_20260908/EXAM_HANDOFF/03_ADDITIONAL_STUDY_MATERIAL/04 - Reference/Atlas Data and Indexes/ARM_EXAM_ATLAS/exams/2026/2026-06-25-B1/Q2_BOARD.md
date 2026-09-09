# E2026-06-25-B1-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `board:adc`, `board:gpio`, `board:joystick`, `board:timer`, `mem:matrix-row-major`, `risk:irq-shared-state`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ADC-SAMPLE-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Exams\Exam 25.06.2206\20260625_ARM_1.pdf`

## Requirement

Build a debounced joystick-driven Bulls and Cows game, seed a four-digit secret from a free-running timer, show the guess and encoded result on LEDs, and retain the secret across guesses.

## Concepts

foreground state machine; timer seed; nibble extraction; two-bit LED fields; debounced joystick events

## Constraints and risks

Physical debounce required; secret captured only once per game; Callbacks capture events only; clear frequency arrays before every call; do not change the secret between guesses.

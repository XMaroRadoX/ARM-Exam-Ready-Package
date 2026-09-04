# E2026-02-18-A2-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `board:adc`, `board:dac`, `board:timer`, `cpu:flags`, `mem:matrix-row-major`, `risk:irq-shared-state`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-CPU-FLAGS-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material 2026\Exams\20260218_ARM_2.pdf`

## Requirement

Implement the three-timer, DAC and 50 ms scheduling variant, including frequency/duration calculations and explicit running/stopped states.

## Concepts

three independent timers; scheduler; DAC table; timing conversion; state machine; resource ownership

## Constraints and risks

50 ms scheduler tick and paper-specific note timing; Separate ISR flags from main processing and keep every timer/vector owner unique.

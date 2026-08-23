# E2026-02-18-A1-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `risk:irq-shared-state`, `risk:vector-ownership`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material 2026\Exams\20260218_ARM_1.pdf`

## Requirement

Coordinate three timers for A/B/C states, stream SinTable[45] through the DAC, use a 50 ms scheduler tick, compute frequency/duration values, and track whether each timer is running.

## Concepts

multi-timer scheduler; timer-running state; waveform streaming; frequency/duration conversion; interrupt-to-main events

## Constraints and risks

50 ms scheduler tick; SinTable[45]; calculated note frequency/duration; Generated/control data must be stable before timers consume it; avoid conflicting ownership of timers and vectors.

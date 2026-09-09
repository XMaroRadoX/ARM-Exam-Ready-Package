# E2026-02-03-A3-Q2

- Delivery: `C + ASM call`
- Tags: `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `cpu:flags`, `mem:word-array`, `risk:irq-shared-state`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-ALG-RECURRENCE-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-CPU-FLAGS-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material 2026\Exams\20260203_ARM_3.pdf`

## Requirement

Read/display ADC data, use KEY2 to generate the sequence, and use a two-second timer to display sequence values on LEDs.

## Concepts

ADC cache; button trigger; periodic sequence playback; LED truncation/scaling

## Constraints and risks

2 s sequence interval; Sequence array element width must match ASM; start playback only after generation completes.

# E2026-02-03-A2-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `board:adc`, `board:dac`, `board:gpio`, `risk:irq-shared-state`, `state:debounce`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`
- Source: `Material 2026\Exams\20260203_ARM_2.pdf`

## Requirement

Read the potentiometer with ADC, show its high eight bits on LEDs, and invoke the encoder from KEY1 with the required debounce behavior.

## Concepts

ADC cache; LED scaling; debounced button; C/ASM buffer handoff

## Constraints and risks

Physical debounce required; Use fixed-width types and a stable input buffer.

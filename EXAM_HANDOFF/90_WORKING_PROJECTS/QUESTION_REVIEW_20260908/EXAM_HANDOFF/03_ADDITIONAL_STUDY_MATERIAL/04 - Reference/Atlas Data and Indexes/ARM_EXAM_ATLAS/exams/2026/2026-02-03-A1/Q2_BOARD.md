# E2026-02-03-A1-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `board:adc`, `board:dac`, `board:gpio`, `risk:irq-shared-state`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`
- Source: `Material 2026\Exams\20260203_ARM_1.pdf`

## Requirement

Read the potentiometer through ADC, show the top eight bits on LEDs, and on INT0 call the assembly routine with physical debouncing enabled.

## Concepts

ADC sampling/cache; bit scaling; LED output; debounced external interrupt; C/ASM call

## Constraints and risks

Physical debounce required; Pass a stable snapshot/buffer to ASM; separate ISR event capture from long processing.

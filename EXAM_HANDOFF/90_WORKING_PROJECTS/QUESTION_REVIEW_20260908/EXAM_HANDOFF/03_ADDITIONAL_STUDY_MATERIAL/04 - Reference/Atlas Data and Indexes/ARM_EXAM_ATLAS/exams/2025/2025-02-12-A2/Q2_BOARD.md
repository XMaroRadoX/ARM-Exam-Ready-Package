# E2025-02-12-A2-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `risk:irq-shared-state`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\24-25\2025_02_12\20250212_ARM2.pdf`

## Requirement

Use KEY1 to generate the waveform, configure Timer1 every 1592 cycles, and stream the table through the DAC according to the stated trigger behavior.

## Concepts

button trigger; periodic timer; DAC waveform; table index wrap

## Constraints and risks

Timer1 period 1592 cycles; Array length/scale contract between C and ASM.

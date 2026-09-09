# E2025-02-12-A1-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:fixed-point`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `mem:matrix-row-major`, `risk:irq-shared-state`, `state:debounce`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\24-25\2025_02_12\20250212_ARM1.pdf`

## Requirement

On INT0, call the assembly generator for sineValues[45]; configure Timer0 every 1263 cycles and stream the samples to the DAC; no debouncing is required.

## Concepts

waveform table; periodic timer; DAC output; explicit no-debounce requirement; ISR/main coordination

## Constraints and risks

Timer0 period 1263 cycles; 45 samples; Array type/length and fixed-point-to-DAC conversion must match the ASM output.

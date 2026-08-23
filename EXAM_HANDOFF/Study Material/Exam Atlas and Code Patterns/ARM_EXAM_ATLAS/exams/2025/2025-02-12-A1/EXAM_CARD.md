# E2025-02-12-A1

- Date: `2025-02-12`
- Variant: `ARM1`
- Source PDF: `Exams/24-25/2025_02_12/20250212_ARM1.pdf`
- SHA-256: `04bdc71658fd0d480ff738ea259fb791ea48991a1e45b2f4d8ec082de65a597f`
- Answer collection: `Study Material/Solved Exams/2025-02-12_ARM1_Sine_DAC`
- Tags: `abi:nonleaf`, `alg:fixed-point`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `cpu:flags`, `mem:matrix-row-major`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2026-02-18-A2`, `E2026-02-03-A3`, `E2025-02-12-A2`, `E2026-06-25-B1`, `E2026-02-18-A1`

## Questions

### Q1 - ASM

Generate sine values with the stated Maclaurin/fixed-point recurrence, maintaining scale, signs, loop limits and array storage.

**Traps:** Define fixed-point scale and 32/64-bit intermediate register pairs.

### Q2 - C + ASM call

On INT0, call the assembly generator for sineValues[45]; configure Timer0 every 1263 cycles and stream the samples to the DAC; no debouncing is required.

**Traps:** Array type/length and fixed-point-to-DAC conversion must match the ASM output.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

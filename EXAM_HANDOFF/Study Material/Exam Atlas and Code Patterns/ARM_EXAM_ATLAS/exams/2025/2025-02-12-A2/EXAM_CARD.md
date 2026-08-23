# E2025-02-12-A2

- Date: `2025-02-12`
- Variant: `ARM2`
- Source PDF: `Material (8)\Exams\24-25\2025_02_12\20250212_ARM2.pdf`
- SHA-256: `6260e7e253a7ddd3c5e186b84f08ef3366e0f4d062501001dadd1abb872a8b10`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2025-02-12_ARM2_Cosine_DAC`
- Tags: `abi:nonleaf`, `alg:fixed-point`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2025-02-12-A1`, `E2026-02-18-A1`, `E2026-02-03-A3`, `E2026-02-18-A2`, `E2026-06-25-B1`

## Questions

### Q1 - ASM

Generate cosine values with the required fixed-point recurrence, scale and array bounds.

**Traps:** Return/array convention and intermediate width must be documented.

### Q2 - C + ASM call

Use KEY1 to generate the waveform, configure Timer1 every 1592 cycles, and stream the table through the DAC according to the stated trigger behavior.

**Traps:** Array length/scale contract between C and ASM.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

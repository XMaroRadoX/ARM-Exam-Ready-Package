# E2026-02-03-A3

- Date: `2026-02-03`
- Variant: `ARM3`
- Source PDF: `Exams/Exam 03.02.2026/20260203_ARM_3.pdf`
- SHA-256: `3b7d7638803bf8e8c0329eca34265667b4df7ad4c19a500b45b0e1566074d46b`
- Answer collection: `Study Material/Solved Exams/2026-02-03_ARM1_LookAndSay_ADC`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `cpu:flags`, `flow:nested-loop`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2026-02-18-A2`, `E2026-02-18-A1`, `E2025-02-12-A1`, `E2026-02-03-A1`, `E2025-07-01-A1`

## Questions

### Q1 - ASM

Fill a word array with the Recaman sequence, selecting subtraction only when positive and not already present, otherwise addition.

**Traps:** Pointer/length input and returned count/status; preserve outer index during duplicate-search helper.

### Q2 - C + ASM call

Read/display ADC data, use KEY2 to generate the sequence, and use a two-second timer to display sequence values on LEDs.

**Traps:** Sequence array element width must match ASM; start playback only after generation completes.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

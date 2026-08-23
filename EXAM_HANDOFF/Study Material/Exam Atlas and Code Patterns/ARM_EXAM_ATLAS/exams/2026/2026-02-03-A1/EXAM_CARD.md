# E2026-02-03-A1

- Date: `2026-02-03`
- Variant: `ARM1`
- Source PDF: `Exams/Exam 03.02.2026/20260203_ARM_1.pdf`
- SHA-256: `4d1f2a9349357a96f0785b83bf347553e73bcd551ccac6d4086dbe5a545488f4`
- Answer collection: `Study Material/Solved Exams/2026-02-03_ARM1_LookAndSay_ADC`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `cpu:flags`, `mem:byte-array`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`
- Related exams: `E2026-02-03-A3`, `E2025-02-12-A1`, `E2026-02-18-A2`, `E2026-02-18-A1`, `E2026-02-03-A2`

## Questions

### Q1 - ASM

Generate the Look-and-Say sequence in the required digit representation, grouping equal runs and writing count/value pairs without overrunning the output buffer.

**Traps:** Input/output pointers, lengths and returned new length must be explicit; preserve live pointers across helpers.

### Q2 - C + ASM call

Read the potentiometer through ADC, show the top eight bits on LEDs, and on INT0 call the assembly routine with physical debouncing enabled.

**Traps:** Pass a stable snapshot/buffer to ASM; separate ISR event capture from long processing.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

# E2026-02-03-A2

- Date: `2026-02-03`
- Variant: `ARM2`
- Source PDF: `Material 2026\Exams\20260203_ARM_2.pdf`
- SHA-256: `ecc909cda345d5f4bbd6c6978f0417a8921c5647290b8feaadba497438a44829`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2026-02-03_ARM2_RLE_ADC`
- Tags: `abi:nonleaf`, `board:adc`, `board:dac`, `board:gpio`, `flow:early-break`, `mem:byte-array`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`
- Related exams: `E2026-02-03-A1`, `E2025-02-12-A1`, `E2026-06-25-B2`, `E2026-06-25-B1`, `E2026-02-18-A1`

## Questions

### Q1 - ASM

Run-length encode the digit array into the required count/value format, including final-run handling and output length.

**Traps:** Define source length, destination capacity and returned encoded length.

### Q2 - C + ASM call

Read the potentiometer with ADC, show its high eight bits on LEDs, and invoke the encoder from KEY1 with the required debounce behavior.

**Traps:** Use fixed-width types and a stable input buffer.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

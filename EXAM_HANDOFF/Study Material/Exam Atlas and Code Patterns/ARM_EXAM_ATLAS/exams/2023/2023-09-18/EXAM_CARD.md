# E2023-09-18

- Date: `2023-09-18`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230918 arm.pdf`
- SHA-256: `2e6568d814b67ff734004e311accb982e610ba7544cdb5f1f91b324981b7846b`
- Answer collection: `Study Material/Solved Exams/2023-09-18_DigitAddition_Buttons`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:gpio`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`
- Related exams: `E2024-09-16`, `E2024-02-12`, `E2026-02-03-A3`, `E2026-02-03-A1`, `E2025-02-12-A1`

## Questions

### Q1 - ASM

Implement digitSum and digitaddition so one assembly subroutine calls another and reports arithmetic overflow correctly.

**Traps:** Save LR before nested BL; preserve R4-R11; return values and status must be defined.

### Q2 - C + ASM call

Use KEY1 and KEY2 to build a binary value K, trigger processing from INT0, manage arrays, call assembly and show the comparison result on LEDs.

**Traps:** Do not call long assembly work directly from an ISR unless the exam demands it.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

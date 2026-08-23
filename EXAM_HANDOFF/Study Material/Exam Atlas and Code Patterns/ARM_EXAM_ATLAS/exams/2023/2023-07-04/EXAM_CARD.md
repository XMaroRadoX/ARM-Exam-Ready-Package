# E2023-07-04

- Date: `2023-07-04`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230704 arm.pdf`
- SHA-256: `00b04fb9ee48348d35f760dc4be463f251c7e107e6fece712f732e2ce8e0a82c`
- Answer collection: `Study Material/Solved Exams/2023-07-04_Sociable_Timer`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:gpio`, `board:timer`, `flow:nested-loop`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2026-02-03-A3`, `E2026-06-25-B2`, `E2026-02-18-A1`, `E2025-07-01-A2`, `E2025-07-01-A1`

## Questions

### Q1 - ASM

Compute aliquot sums and detect a sociable-number sequence using divisor tests, nested loops and subroutine calls.

**Traps:** Nested BL calls must preserve LR; loop state belongs in callee-saved registers or stack slots.

### Q2 - C + ASM call

Configure Timer1 for a two-second periodic event, advance a circular sequence array, call the assembly routine, and display the result on LEDs.

**Traps:** Shared buffers and integer widths must match ASM declarations.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

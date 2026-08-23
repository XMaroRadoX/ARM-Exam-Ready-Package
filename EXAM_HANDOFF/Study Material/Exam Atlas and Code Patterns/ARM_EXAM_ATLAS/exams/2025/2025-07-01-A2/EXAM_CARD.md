# E2025-07-01-A2

- Date: `2025-07-01`
- Variant: `ARM2`
- Source PDF: `Exams/24-25/2025_07_01/ARM2.pdf`
- SHA-256: `61b5bc6866d95a1ce17fd0356cb661d342641945037f71924afc4050cfba1e81`
- Answer collection: `Study Material/Solved Exams/2025-07-01_ARM1_LCG_Rhythm`
- Tags: `abi:nonleaf`, `abi:stacked-args`, `alg:recurrence`, `board:gpio`, `board:joystick`, `board:timer`, `flow:nested-loop`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`
- Related exams: `E2025-07-01-A1`, `E2026-06-25-B2`, `E2026-02-03-A3`, `E2023-07-04`, `E2026-06-25-B1`

## Questions

### Q1 - ASM

Implement the variant LCG with its shift operation and five-argument interface, preserving the specified arithmetic order.

**Traps:** Fifth argument offset depends on prologue; preserve callee-saved registers and stack alignment.

### Q2 - ASM startup

Drive the variant generator from Reset_Handler with correct argument construction and persistent loop state.

**Traps:** Eight-byte alignment and exact cleanup of argument 5 are mandatory.

### Q3 - C

Use Timer1 for a 2.5-second LED sequence and process only the joystick's first movement in the game logic.

**Traps:** N/A

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

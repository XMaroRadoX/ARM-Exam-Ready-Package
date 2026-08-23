# E2023-05-17

- Date: `2023-05-17`
- Variant: `ARM`
- Source PDF: `Material (8)\Exams\22-23\20230517 arm.pdf`
- SHA-256: `94a30856a4f9a56bb908dbab2def2de9fee9973a4471ac5111399a992509bbab`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2023-05-17_Signed_64_Division`
- Tags: `abi:nonleaf`, `board:adc`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`
- Related exams: `E2026-02-18-A2`, `E2026-02-03-A3`, `E2025-02-12-A1`, `E2024-09-16`, `E2024-02-12`

## Questions

### Q1 - ASM

Divide a signed 64-bit dividend by a signed 32-bit divisor without MUL, using sign normalization, a 64-bit shift/subtract loop, and quotient-bit construction.

**Traps:** Document two-register 64-bit values and preserved working registers.

### Q2 - ASM flags

Set or report the required N, Z, C and V status according to the division outcome using program-status-register operations.

**Traps:** Flags are caller-clobbered; required output contract must be explicit.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

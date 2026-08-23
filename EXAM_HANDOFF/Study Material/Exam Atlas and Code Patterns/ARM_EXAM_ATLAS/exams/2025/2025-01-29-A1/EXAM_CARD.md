# E2025-01-29-A1

- Date: `2025-01-29`
- Variant: `ARM1`
- Source PDF: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM1.pdf`
- SHA-256: `81b1160be1d5b7aa4520486427166188d838607a3f22089c7b04734b3dad4575`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2025-01-29_ARM1_Affine_Two_Timers`
- Tags: `abi:nonleaf`, `alg:fixed-point`, `board:gpio`, `board:timer`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2025-01-29-A3`, `E2025-01-29-A2`, `E2024-02-28`, `E2024-02-12`, `E2026-06-25-B2`

## Questions

### Q1 - ASM

Apply the requested bitwise affine transformation to a packed 8x8 binary matrix while preserving the specified bit and row order.

**Traps:** Pointer and output contract must state byte order and whether in-place update is allowed.

### Q2 - C + ASM call

Run Timer1 freely with reset at 0xFFFF and no IRQ; INT0 collects bytes and XORs/displays them; KEY1 calls the assembly transform; Timer0 blinks rows with a 0.5-second full period.

**Traps:** Match packed-array pointer and size types; keep ISR work bounded.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

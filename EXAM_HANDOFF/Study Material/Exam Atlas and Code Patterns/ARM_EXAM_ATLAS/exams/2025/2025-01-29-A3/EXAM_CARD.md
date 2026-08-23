# E2025-01-29-A3

- Date: `2025-01-29`
- Variant: `ARM3`
- Source PDF: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM3.pdf`
- SHA-256: `761ce33d98721985812e9dac30fedd846893bfc2ccbc7b16513615d24cde2a6e`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2025-01-29_ARM3_Transpose_Timer`
- Tags: `abi:nonleaf`, `board:dac`, `board:gpio`, `board:timer`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-DAC-STREAM-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2024-02-12`, `E2026-06-25-B2`, `E2026-06-25-B1`, `E2025-01-29-A1`, `E2024-02-28`

## Questions

### Q1 - ASM

Transpose a packed binary matrix by exchanging row/column bit coordinates without corrupting unrelated bits.

**Traps:** Document input/output aliasing and packed layout.

### Q2 - C + ASM call

Use Timer2 and KEY1/KEY2 to fill arrays, then use INT0 to verify the requested algebraic property and display pass/fail on LEDs.

**Traps:** Assembly receives complete buffers and returns a defined Boolean/status.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

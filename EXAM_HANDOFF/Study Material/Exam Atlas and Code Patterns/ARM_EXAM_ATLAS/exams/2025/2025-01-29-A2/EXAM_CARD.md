# E2025-01-29-A2

- Date: `2025-01-29`
- Variant: `ARM2`
- Source PDF: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM2.pdf`
- SHA-256: `af077d82dca1acfbbac322ee1774a4d6c4ec796d42721c073e0b0fc20543e50b`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2025-01-29_ARM2_Matrix_Two_Timers`
- Tags: `board:gpio`, `board:timer`, `cpu:flags`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2024-02-12`, `E2025-01-29-A3`, `E2025-01-29-A1`, `E2026-06-25-B2`, `E2024-02-28`

## Questions

### Q1 - ASM

Multiply two packed binary matrices using bit-level dot products and store the packed result with the required orientation.

**Traps:** Three matrix pointers and dimensions must fit the chosen interface without clobbering live loop state.

### Q2 - C + ASM call

Use the specified free-running timer and interrupts to fill matrices A and B; invoke multiplication on KEY1; display result rows on LEDs every 0.5 seconds.

**Traps:** Do not expose partially filled buffers to ASM; use a ready flag or count.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

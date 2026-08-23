# E2024-02-12

- Date: `2024-02-12`
- Variant: `ARM`
- Source PDF: `Material (8)\Exams\23-24\20240212 arm.pdf`
- SHA-256: `857211aa08989b7cd8e4630443c80fe33a4ad8e94d34a17636626deac8230ede`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2024-02-12_Maze_LCG_Timer`
- Tags: `abi:nonleaf`, `alg:graph-search`, `board:gpio`, `board:timer`, `cpu:flags`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`
- Related exams: `E2025-01-29-A3`, `E2024-09-16`, `E2026-06-25-B2`, `E2025-01-29-A2`, `E2024-02-28`

## Questions

### Q1 - ASM

Solve a two-dimensional byte maze by repeatedly propagating reachable distances until the destination is reached or no progress remains.

**Traps:** Matrix base, dimensions and result contract must be explicit; preserve loop state across helpers.

### Q2 - C + ASM call

Generate a random maze with an LCG seeded from a free-running Timer0, start from KEY2, fill the byte matrix safely, and call the assembly solver.

**Traps:** Pass base pointer and dimensions in the agreed argument registers; define byte element type.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

# E2024-07-09

- Date: `2024-07-09`
- Variant: `ARM`
- Source PDF: `Exams/23-24/20240709 arm.pdf`
- SHA-256: `072489aedf62543620d5bb60295fb085204bae358d5316fb342c1150475a9a98`
- Answer collection: `Study Material/Solved Exams/2024-07-09_DFS_SysTick`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `alg:graph-search`, `alg:recurrence`, `board:timer`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`, `timing:periodic`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2024-02-28`, `E2025-01-29-A3`, `E2025-01-29-A1`, `E2024-09-16`, `E2024-02-12`

## Questions

### Q1 - ASM

Solve a maze with depth-first search using an explicit stack, four parameters and a nested call to chooseNeighbor.

**Traps:** R0-R3 are arguments; save LR and live caller-saved values before chooseNeighbor; keep SP eight-byte aligned.

### Q2 - ASM startup/exception

Configure SysTick directly in Reset_Handler, collect available moves, choose one using modulo arithmetic, and keep the stack balanced across all branches.

**Traps:** Reset context and handler ownership differ from ordinary C calls; every path must restore SP.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

# E2024-02-28

- Date: `2024-02-28`
- Variant: `ARM`
- Source PDF: `Exams/23-24/20240228 arm.pdf`
- SHA-256: `772f6c10718ce63a360fd71027fbfce97bacac7b86829e48cf4bd3763d966783`
- Answer collection: `Study Material/Solved Exams/2024-02-28_ShortestPath_Timer`
- Tags: `abi:nonleaf`, `alg:graph-search`, `alg:recurrence`, `board:gpio`, `board:timer`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2025-01-29-A3`, `E2024-02-12`, `E2026-02-03-A3`, `E2025-01-29-A1`, `E2024-09-16`

## Questions

### Q1 - ASM

Compute a shortest path through a two-dimensional byte maze while respecting walls, bounds and distance updates.

**Traps:** Define matrix layout, dimensions, start/end and failure return value.

### Q2 - C

Configure a timer for a 0.5-second sequence and move an LED indication through the required states without losing events.

**Traps:** N/A except ISR/main shared-state rules.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

# E2024-09-16

- Date: `2024-09-16`
- Variant: `ARM`
- Source PDF: `Exams/23-24/20240916 arm.pdf`
- SHA-256: `bbadd5254928052d8fdf6f824af902ed80a57c58adbb8028e7ec666d2935e3c1`
- Answer collection: `Study Material/Solved Exams/2024-09-16_Kruskal_Buttons`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `abi:stacked-args`, `alg:graph-search`, `board:gpio`, `cpu:flags`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`
- Related exams: `E2024-02-12`, `E2025-01-29-A3`, `E2024-02-28`, `E2023-09-18`, `E2026-06-25-B2`

## Questions

### Q1 - ASM

Implement the Kruskal-style maze operation across three arrays with seven parameters, including min/max selection, component replacement and row-major access.

**Traps:** R0-R3 carry the first four arguments; arguments 5-7 are loaded from the caller stack at offsets adjusted for the callee prologue; SP remains eight-byte aligned.

### Q2 - C

Implement a two-button state machine that increments a value and applies the required offset while handling event order and button behavior.

**Traps:** N/A

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

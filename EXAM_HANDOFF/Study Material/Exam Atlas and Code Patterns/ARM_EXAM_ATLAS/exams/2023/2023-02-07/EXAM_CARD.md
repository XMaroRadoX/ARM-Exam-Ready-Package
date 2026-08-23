# E2023-02-07

- Date: `2023-02-07`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230207 arm.pdf`
- SHA-256: `77929b413afda671274838630078b32bbebe1e643e1102a00412a7209879ce26`
- Answer collection: `Study Material/Solved Exams/2023-02-07_Sort_FreeRunning_Timer`
- Tags: `abi:nonleaf`, `alg:sorting`, `board:gpio`, `board:timer`, `cpu:svc`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `risk:vector-ownership`, `state:debounce`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-SORTING-001`, `PAT-CPU-SVC-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`
- Related exams: `E2024-02-12`, `E2026-06-25-B2`, `E2025-01-29-A3`, `E2025-01-29-A2`, `E2025-01-29-A1`

## Questions

### Q1 - ASM

Copy signed byte values into a working array, then perform insertion sort while preserving signed ordering and array bounds.

**Traps:** Preserve callee-saved registers; return cleanly through LR when split into helpers.

### Q2 - C + ASM call

Use Timer1 as a free-running counter reset at 0xFF without an IRQ; INT0 captures array data and alternates LEDs 6/7; KEY1 invokes the assembly sort.

**Traps:** C prototype must match ASM symbol and argument registers.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

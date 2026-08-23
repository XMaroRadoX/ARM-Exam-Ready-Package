# E2023-02-24

- Date: `2023-02-24`
- Variant: `ARM`
- Source PDF: `Material (8)\Exams\22-23\20230224 arm.pdf`
- SHA-256: `ebd2df9c75ec7e24bd6f76515a3b06cdfcec78b7e5aea7d33d977761fa0dc0a4`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2023-02-24_Kaprekar_SVC`
- Tags: `abi:nonleaf`, `alg:recurrence`, `alg:sorting`, `cpu:exception-frame`, `cpu:svc`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-SORTING-001`, `PAT-CPU-EXCEPTION-FRAME-001`, `PAT-CPU-SVC-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`
- Related exams: `E2024-07-09`, `E2024-02-28`, `E2023-02-07`, `E2025-01-29-A3`, `E2025-01-29-A1`

## Questions

### Q1 - ASM

Implement the Kaprekar digit transformation, including digit extraction, reordering, subtraction and repeated convergence logic.

**Traps:** Nested helper calls require LR protection and callee-saved discipline.

### Q2 - ASM exception

Handle SVC #50, locate the correct exception stack frame, decode the SVC immediate from the instruction before stacked PC, repeatedly call the Kaprekar routine, and return the iteration count in R6.

**Traps:** Preserve EXC_RETURN in LR and distinguish handler stack frame from normal AAPCS frame.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.

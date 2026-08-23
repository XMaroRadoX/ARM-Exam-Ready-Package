# E2023-02-24-Q2

- Delivery: `ASM exception`
- Tags: `abi:nonleaf`, `alg:recurrence`, `cpu:exception-frame`, `cpu:svc`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-EXCEPTION-FRAME-001`, `PAT-CPU-SVC-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\22-23\20230224 arm.pdf`

## Requirement

Handle SVC #50, locate the correct exception stack frame, decode the SVC immediate from the instruction before stacked PC, repeatedly call the Kaprekar routine, and return the iteration count in R6.

## Concepts

SVC decode; MSP/PSP selection; stacked PC; exception return; nested calls

## Constraints and risks

N/A; Preserve EXC_RETURN in LR and distinguish handler stack frame from normal AAPCS frame.

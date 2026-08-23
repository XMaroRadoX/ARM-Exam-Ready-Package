# E2026-02-03-A1-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:recurrence`, `cpu:flags`, `mem:byte-array`, `mem:word-array`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material 2026\Exams\20260203_ARM_1.pdf`

## Requirement

Generate the Look-and-Say sequence in the required digit representation, grouping equal runs and writing count/value pairs without overrunning the output buffer.

## Concepts

digit array; run grouping; two-pointer loop; output bounds; recurrence

## Constraints and risks

N/A; Input/output pointers, lengths and returned new length must be explicit; preserve live pointers across helpers.

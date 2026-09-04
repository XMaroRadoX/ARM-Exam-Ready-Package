# E2023-02-07-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:sorting`, `cpu:svc`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-SORTING-001`, `PAT-CPU-SVC-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\22-23\20230207 arm.pdf`

## Requirement

Copy signed byte values into a working array, then perform insertion sort while preserving signed ordering and array bounds.

## Concepts

byte arrays; signed comparison; insertion sort; nested loops; address arithmetic

## Constraints and risks

N/A; Preserve callee-saved registers; return cleanly through LR when split into helpers.

# E2025-07-01-A2-Q1

- Delivery: `ASM`
- Tags: `abi:stacked-args`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-STACKED-ARGS-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\24-25\2025_07_01\ARM2.pdf`

## Requirement

Implement the variant LCG with its shift operation and five-argument interface, preserving the specified arithmetic order.

## Concepts

LCG; shifts; five arguments; stacked fifth argument; unsigned wraparound/modulo

## Constraints and risks

N/A; Fifth argument offset depends on prologue; preserve callee-saved registers and stack alignment.

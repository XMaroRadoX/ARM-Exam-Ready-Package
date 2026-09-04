# E2024-09-16-Q1

- Delivery: `ASM`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `abi:stacked-args`, `alg:graph-search`, `cpu:flags`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\23-24\20240916 arm.pdf`

## Requirement

Implement the Kruskal-style maze operation across three arrays with seven parameters, including min/max selection, component replacement and row-major access.

## Concepts

three arrays; seven arguments; stacked arguments; min/max; replace scan; row-major indexing

## Constraints and risks

N/A; R0-R3 carry the first four arguments; arguments 5-7 are loaded from the caller stack at offsets adjusted for the callee prologue; SP remains eight-byte aligned.

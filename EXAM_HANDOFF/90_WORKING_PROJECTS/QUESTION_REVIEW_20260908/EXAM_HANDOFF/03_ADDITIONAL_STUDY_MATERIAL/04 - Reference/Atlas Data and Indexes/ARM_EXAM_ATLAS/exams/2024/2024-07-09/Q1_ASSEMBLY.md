# E2024-07-09-Q1

- Delivery: `ASM`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `alg:graph-search`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\23-24\20240709 arm.pdf`

## Requirement

Solve a maze with depth-first search using an explicit stack, four parameters and a nested call to chooseNeighbor.

## Concepts

DFS; explicit software stack; 2D matrix; four arguments; nested call; backtracking

## Constraints and risks

N/A; R0-R3 are arguments; save LR and live caller-saved values before chooseNeighbor; keep SP eight-byte aligned.

# E2024-02-12-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:graph-search`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\23-24\20240212 arm.pdf`

## Requirement

Solve a two-dimensional byte maze by repeatedly propagating reachable distances until the destination is reached or no progress remains.

## Concepts

row-major 2D byte matrix; neighbor checks; repeated passes; sentinel values; nested loops

## Constraints and risks

N/A; Matrix base, dimensions and result contract must be explicit; preserve loop state across helpers.

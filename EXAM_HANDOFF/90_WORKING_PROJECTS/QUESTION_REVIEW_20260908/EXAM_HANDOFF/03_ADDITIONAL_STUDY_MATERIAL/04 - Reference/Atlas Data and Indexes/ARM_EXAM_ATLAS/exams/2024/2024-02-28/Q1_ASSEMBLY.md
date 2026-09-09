# E2024-02-28-Q1

- Delivery: `ASM`
- Tags: `abi:nonleaf`, `alg:graph-search`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\23-24\20240228 arm.pdf`

## Requirement

Compute a shortest path through a two-dimensional byte maze while respecting walls, bounds and distance updates.

## Concepts

2D byte matrix; shortest-path wavefront; neighbor selection; termination

## Constraints and risks

N/A; Define matrix layout, dimensions, start/end and failure return value.

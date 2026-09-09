# E2023-05-17-Q2

- Delivery: `ASM flags`
- Tags: `abi:nonleaf`, `cpu:flags`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-CPU-FLAGS-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\22-23\20230517 arm.pdf`

## Requirement

Set or report the required N, Z, C and V status according to the division outcome using program-status-register operations.

## Concepts

APSR observation/manipulation; overflow; result classification

## Constraints and risks

N/A; Flags are caller-clobbered; required output contract must be explicit.

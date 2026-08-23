# E2023-05-17-Q1

- Delivery: `ASM`
- Tags: `board:adc`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-ADC-SAMPLE-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-AAPCS-STACK-SAFETY-001`
- Source: `Material (8)\Exams\22-23\20230517 arm.pdf`

## Requirement

Divide a signed 64-bit dividend by a signed 32-bit divisor without MUL, using sign normalization, a 64-bit shift/subtract loop, and quotient-bit construction.

## Concepts

signed 64-bit arithmetic; two-word shifts; restoring division; two's complement

## Constraints and risks

N/A; Document two-register 64-bit values and preserved working registers.

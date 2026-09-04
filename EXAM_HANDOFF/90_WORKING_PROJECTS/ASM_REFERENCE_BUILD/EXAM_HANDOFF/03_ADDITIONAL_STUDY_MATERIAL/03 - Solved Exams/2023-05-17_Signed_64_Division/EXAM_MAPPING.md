# Exam mapping

- Exam ID: `E2023-05-17`
- Questions: `E2023-05-17-Q1`, `E2023-05-17-Q2`
- Tags: `abi:nonleaf`, `board:adc`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:stack-alignment`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2023-05-17-Q1` | Divide a signed 64-bit dividend by a signed 32-bit divisor without MUL, using sign normalization, a 64-bit shift/subtract loop, and quotient-bit construction. | `Material (8)\Exams\22-23\20230517 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2023-05-17-Q2` | Set or report the required N, Z, C and V status according to the division outcome using program-status-register operations. | `Material (8)\Exams\22-23\20230517 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

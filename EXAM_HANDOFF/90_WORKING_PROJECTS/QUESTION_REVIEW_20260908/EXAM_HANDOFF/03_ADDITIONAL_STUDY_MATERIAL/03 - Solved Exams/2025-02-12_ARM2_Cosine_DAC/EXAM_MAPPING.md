# Exam mapping

- Exam ID: `E2025-02-12-A2`
- Questions: `E2025-02-12-A2-Q1`, `E2025-02-12-A2-Q2`
- Tags: `abi:nonleaf`, `alg:fixed-point`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2025-02-12-A2-Q1` | Generate cosine values with the required fixed-point recurrence, scale and array bounds. | `Material (8)\Exams\24-25\2025_02_12\20250212_ARM2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-02-12-A2-Q2` | Use KEY1 to generate the waveform, configure Timer1 every 1592 cycles, and stream the table through the DAC according to the stated trigger behavior. | `Material (8)\Exams\24-25\2025_02_12\20250212_ARM2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

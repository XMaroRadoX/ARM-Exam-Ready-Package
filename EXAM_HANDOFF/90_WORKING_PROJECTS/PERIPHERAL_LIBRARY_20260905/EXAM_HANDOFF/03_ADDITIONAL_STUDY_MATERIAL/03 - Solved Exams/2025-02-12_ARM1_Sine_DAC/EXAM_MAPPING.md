# Exam mapping

- Exam ID: `E2025-02-12-A1`
- Questions: `E2025-02-12-A1-Q1`, `E2025-02-12-A1-Q2`
- Tags: `abi:nonleaf`, `alg:fixed-point`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `cpu:flags`, `mem:matrix-row-major`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2025-02-12-A1-Q1` | Generate sine values with the stated Maclaurin/fixed-point recurrence, maintaining scale, signs, loop limits and array storage. | `Material (8)\Exams\24-25\2025_02_12\20250212_ARM1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-02-12-A1-Q2` | On INT0, call the assembly generator for sineValues[45]; configure Timer0 every 1263 cycles and stream the samples to the DAC; no debouncing is required. | `Material (8)\Exams\24-25\2025_02_12\20250212_ARM1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

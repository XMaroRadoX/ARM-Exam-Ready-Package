# Exam mapping

- Exam ID: `E2026-02-18-A2`
- Questions: `E2026-02-18-A2-Q1`, `E2026-02-18-A2-Q2`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `alg:recurrence`, `board:adc`, `board:dac`, `board:timer`, `cpu:flags`, `mem:matrix-row-major`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2026-02-18-A2-Q1` | Generate the Hofstadter-Conway variant iteratively in a word array with correct seeds, recurrence-derived indexes and requested aggregate/result. | `Material 2026\Exams\20260218_ARM_2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2026-02-18-A2-Q2` | Implement the three-timer, DAC and 50 ms scheduling variant, including frequency/duration calculations and explicit running/stopped states. | `Material 2026\Exams\20260218_ARM_2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

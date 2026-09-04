# Exam mapping

- Exam ID: `E2026-02-03-A3`
- Questions: `E2026-02-03-A3-Q1`, `E2026-02-03-A3-Q2`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `cpu:flags`, `flow:nested-loop`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2026-02-03-A3-Q1` | Fill a word array with the Recaman sequence, selecting subtraction only when positive and not already present, otherwise addition. | `Material 2026\Exams\20260203_ARM_3.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2026-02-03-A3-Q2` | Read/display ADC data, use KEY2 to generate the sequence, and use a two-second timer to display sequence values on LEDs. | `Material 2026\Exams\20260203_ARM_3.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

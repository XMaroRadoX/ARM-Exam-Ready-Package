# Exam mapping

- Exam ID: `E2026-02-03-A1`
- Questions: `E2026-02-03-A1-Q1`, `E2026-02-03-A1-Q2`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `cpu:flags`, `mem:byte-array`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2026-02-03-A1-Q1` | Generate the Look-and-Say sequence in the required digit representation, grouping equal runs and writing count/value pairs without overrunning the output buffer. | `Material 2026\Exams\20260203_ARM_1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2026-02-03-A1-Q2` | Read the potentiometer through ADC, show the top eight bits on LEDs, and on INT0 call the assembly routine with physical debouncing enabled. | `Material 2026\Exams\20260203_ARM_1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

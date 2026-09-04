# Exam mapping

- Exam ID: `E2026-02-18-A1`
- Questions: `E2026-02-18-A1-Q1`, `E2026-02-18-A1-Q2`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `risk:vector-ownership`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2026-02-18-A1-Q1` | Generate the iterative Hofstadter Q sequence in a word array and return or track the required maximum while handling early indices safely. | `Material 2026\Exams\20260218_ARM_1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2026-02-18-A1-Q2` | Coordinate three timers for A/B/C states, stream SinTable[45] through the DAC, use a 50 ms scheduler tick, compute frequency/duration values, and track whether each timer is running. | `Material 2026\Exams\20260218_ARM_1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

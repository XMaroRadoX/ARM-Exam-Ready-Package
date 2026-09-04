# Exam mapping

- Exam ID: `E2026-02-03-A2`
- Questions: `E2026-02-03-A2-Q1`, `E2026-02-03-A2-Q2`
- Tags: `abi:nonleaf`, `board:adc`, `board:dac`, `board:gpio`, `flow:early-break`, `mem:byte-array`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-DAC-STREAM-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2026-02-03-A2-Q1` | Run-length encode the digit array into the required count/value format, including final-run handling and output length. | `Material 2026\Exams\20260203_ARM_2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2026-02-03-A2-Q2` | Read the potentiometer with ADC, show its high eight bits on LEDs, and invoke the encoder from KEY1 with the required debounce behavior. | `Material 2026\Exams\20260203_ARM_2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

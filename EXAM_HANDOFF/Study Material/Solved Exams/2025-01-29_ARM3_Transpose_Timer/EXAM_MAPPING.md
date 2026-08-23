# Exam mapping

- Exam ID: `E2025-01-29-A3`
- Questions: `E2025-01-29-A3-Q1`, `E2025-01-29-A3-Q2`
- Tags: `abi:nonleaf`, `board:dac`, `board:gpio`, `board:timer`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-DAC-STREAM-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2025-01-29-A3-Q1` | Transpose a packed binary matrix by exchanging row/column bit coordinates without corrupting unrelated bits. | `Material (8)\Exams\24-25\2025_01_29\20250129_ARM3.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-01-29-A3-Q2` | Use Timer2 and KEY1/KEY2 to fill arrays, then use INT0 to verify the requested algebraic property and display pass/fail on LEDs. | `Material (8)\Exams\24-25\2025_01_29\20250129_ARM3.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

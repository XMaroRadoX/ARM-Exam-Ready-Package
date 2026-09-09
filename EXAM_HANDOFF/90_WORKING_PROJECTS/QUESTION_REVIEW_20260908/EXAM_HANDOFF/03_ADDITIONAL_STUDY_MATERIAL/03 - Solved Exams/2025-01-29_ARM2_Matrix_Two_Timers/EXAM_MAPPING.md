# Exam mapping

- Exam ID: `E2025-01-29-A2`
- Questions: `E2025-01-29-A2-Q1`, `E2025-01-29-A2-Q2`
- Tags: `board:gpio`, `board:timer`, `cpu:flags`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2025-01-29-A2-Q1` | Multiply two packed binary matrices using bit-level dot products and store the packed result with the required orientation. | `Material (8)\Exams\24-25\2025_01_29\20250129_ARM2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-01-29-A2-Q2` | Use the specified free-running timer and interrupts to fill matrices A and B; invoke multiplication on KEY1; display result rows on LEDs every 0.5 seconds. | `Material (8)\Exams\24-25\2025_01_29\20250129_ARM2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

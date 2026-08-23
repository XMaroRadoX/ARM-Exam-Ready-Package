# Exam mapping

- Exam ID: `E2023-09-18`
- Questions: `E2023-09-18-Q1`, `E2023-09-18-Q2`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:gpio`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2023-09-18-Q1` | Implement digitSum and digitaddition so one assembly subroutine calls another and reports arithmetic overflow correctly. | `Material (8)\Exams\22-23\20230918 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2023-09-18-Q2` | Use KEY1 and KEY2 to build a binary value K, trigger processing from INT0, manage arrays, call assembly and show the comparison result on LEDs. | `Material (8)\Exams\22-23\20230918 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

# Exam mapping

- Exam ID: `E2025-07-01-A2`
- Questions: `E2025-07-01-A2-Q1`, `E2025-07-01-A2-Q2`, `E2025-07-01-A2-Q3`
- Tags: `abi:nonleaf`, `abi:stacked-args`, `alg:recurrence`, `board:gpio`, `board:joystick`, `board:timer`, `flow:nested-loop`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2025-07-01-A2-Q1` | Implement the variant LCG with its shift operation and five-argument interface, preserving the specified arithmetic order. | `Material (8)\Exams\24-25\2025_07_01\ARM2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-07-01-A2-Q2` | Drive the variant generator from Reset_Handler with correct argument construction and persistent loop state. | `Material (8)\Exams\24-25\2025_07_01\ARM2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-07-01-A2-Q3` | Use Timer1 for a 2.5-second LED sequence and process only the joystick's first movement in the game logic. | `Material (8)\Exams\24-25\2025_07_01\ARM2.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

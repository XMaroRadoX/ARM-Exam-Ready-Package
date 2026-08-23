# Exam mapping

- Exam ID: `E2025-07-01-A1`
- Questions: `E2025-07-01-A1-Q1`, `E2025-07-01-A1-Q2`, `E2025-07-01-A1-Q3`
- Tags: `abi:nonleaf`, `abi:stacked-args`, `alg:recurrence`, `board:gpio`, `board:joystick`, `board:timer`, `cpu:flags`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2025-07-01-A1-Q1` | Implement the requested linear congruential generator with five parameters and correct unsigned wraparound/modulo behavior. | `Material (8)\Exams\24-25\2025_07_01\ARM1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-07-01-A1-Q2` | Call the LCG repeatedly from Reset_Handler and maintain the required sequence/state without violating startup or call conventions. | `Material (8)\Exams\24-25\2025_07_01\ARM1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-07-01-A1-Q3` | Use Timer0 for a three-second LED sequence and accept only the joystick's first movement for the rhythm-game state transition. | `Material (8)\Exams\24-25\2025_07_01\ARM1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

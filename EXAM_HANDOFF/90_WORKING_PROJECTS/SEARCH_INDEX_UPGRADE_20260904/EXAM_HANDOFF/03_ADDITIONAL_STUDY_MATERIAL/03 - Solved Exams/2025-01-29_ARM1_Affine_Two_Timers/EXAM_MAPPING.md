# Exam mapping

- Exam ID: `E2025-01-29-A1`
- Questions: `E2025-01-29-A1-Q1`, `E2025-01-29-A1-Q2`
- Tags: `abi:nonleaf`, `alg:fixed-point`, `board:gpio`, `board:timer`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2025-01-29-A1-Q1` | Apply the requested bitwise affine transformation to a packed 8x8 binary matrix while preserving the specified bit and row order. | `Material (8)\Exams\24-25\2025_01_29\20250129_ARM1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2025-01-29-A1-Q2` | Run Timer1 freely with reset at 0xFFFF and no IRQ; INT0 collects bytes and XORs/displays them; KEY1 calls the assembly transform; Timer0 blinks rows with a 0.5-second full period. | `Material (8)\Exams\24-25\2025_01_29\20250129_ARM1.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

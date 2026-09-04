# Exam mapping

- Exam ID: `E2024-02-28`
- Questions: `E2024-02-28-Q1`, `E2024-02-28-Q2`
- Tags: `abi:nonleaf`, `alg:graph-search`, `alg:recurrence`, `board:gpio`, `board:timer`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2024-02-28-Q1` | Compute a shortest path through a two-dimensional byte maze while respecting walls, bounds and distance updates. | `Material (8)\Exams\23-24\20240228 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2024-02-28-Q2` | Configure a timer for a 0.5-second sequence and move an LED indication through the required states without losing events. | `Material (8)\Exams\23-24\20240228 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

# Exam mapping

- Exam ID: `E2024-02-12`
- Questions: `E2024-02-12-Q1`, `E2024-02-12-Q2`
- Tags: `abi:nonleaf`, `alg:graph-search`, `board:gpio`, `board:timer`, `cpu:flags`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2024-02-12-Q1` | Solve a two-dimensional byte maze by repeatedly propagating reachable distances until the destination is reached or no progress remains. | `Material (8)\Exams\23-24\20240212 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2024-02-12-Q2` | Generate a random maze with an LCG seeded from a free-running Timer0, start from KEY2, fill the byte matrix safely, and call the assembly solver. | `Material (8)\Exams\23-24\20240212 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

# Exam mapping

- Exam ID: `E2024-09-16`
- Questions: `E2024-09-16-Q1`, `E2024-09-16-Q2`
- Tags: `abi:four-register-args`, `abi:nonleaf`, `abi:stacked-args`, `alg:graph-search`, `board:gpio`, `cpu:flags`, `flow:nested-loop`, `mem:byte-array`, `mem:matrix-row-major`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2024-09-16-Q1` | Implement the Kruskal-style maze operation across three arrays with seven parameters, including min/max selection, component replacement and row-major access. | `Material (8)\Exams\23-24\20240916 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2024-09-16-Q2` | Implement a two-button state machine that increments a value and applies the required offset while handling event order and button behavior. | `Material (8)\Exams\23-24\20240916 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

# Exam mapping

- Exam ID: `E2023-02-07`
- Questions: `E2023-02-07-Q1`, `E2023-02-07-Q2`
- Tags: `abi:nonleaf`, `alg:sorting`, `board:gpio`, `board:timer`, `cpu:svc`, `flow:early-break`, `flow:nested-loop`, `mem:byte-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `risk:vector-ownership`, `state:debounce`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-SORTING-001`, `PAT-CPU-SVC-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

| Question | Requirement | Source PDF | Verification |
|---|---|---|---|
| `E2023-02-07-Q1` | Copy signed byte values into a working array, then perform insertion sort while preserving signed ordering and array bounds. | `Material (8)\Exams\22-23\20230207 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |
| `E2023-02-07-Q2` | Use Timer1 as a free-running counter reset at 0xFF without an IRQ; INT0 captures array data and alternates LEDs 6/7; KEY1 invokes the assembly sort. | `Material (8)\Exams\22-23\20230207 arm.pdf` | `COMPILE_ONLY` / `COMPILE_ONLY` / `PHYSICAL_BOARD_NOT_TESTED` |

# E2023-09-18-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:gpio`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:irq-shared-state`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-GPIO-EVENT-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`
- Source: `Material (8)\Exams\22-23\20230918 arm.pdf`

## Requirement

Use KEY1 and KEY2 to build a binary value K, trigger processing from INT0, manage arrays, call assembly and show the comparison result on LEDs.

## Concepts

button state machine; bit construction; arrays; IRQ-to-main event; LED result

## Constraints and risks

Button events; debounce policy must be stated; Do not call long assembly work directly from an ISR unless the exam demands it.

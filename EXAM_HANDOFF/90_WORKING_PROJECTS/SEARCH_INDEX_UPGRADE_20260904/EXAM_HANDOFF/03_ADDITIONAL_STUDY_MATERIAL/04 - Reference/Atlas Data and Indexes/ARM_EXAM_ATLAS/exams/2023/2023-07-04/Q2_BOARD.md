# E2023-07-04-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:recurrence`, `board:gpio`, `board:timer`, `mem:word-array`, `risk:irq-shared-state`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-RECURRENCE-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\22-23\20230704 arm.pdf`

## Requirement

Configure Timer1 for a two-second periodic event, advance a circular sequence array, call the assembly routine, and display the result on LEDs.

## Concepts

periodic timer; circular buffer/index; interrupt-to-main communication; LED encoding

## Constraints and risks

2 s periodic interval; Shared buffers and integer widths must match ASM declarations.

# E2024-02-28-Q2

- Delivery: `C`
- Tags: `alg:graph-search`, `alg:recurrence`, `board:gpio`, `board:timer`, `risk:irq-shared-state`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-RECURRENCE-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\23-24\20240228 arm.pdf`

## Requirement

Configure a timer for a 0.5-second sequence and move an LED indication through the required states without losing events.

## Concepts

periodic timer IRQ; LED state machine; shared index

## Constraints and risks

0.5 s periodic interval; N/A except ISR/main shared-state rules.

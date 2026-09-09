# E2023-02-07-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:sorting`, `board:gpio`, `board:timer`, `flow:nested-loop`, `risk:irq-shared-state`, `risk:vector-ownership`, `state:debounce`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-SORTING-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-TIMER-FREE-RUNNING-001`
- Source: `Material (8)\Exams\22-23\20230207 arm.pdf`

## Requirement

Use Timer1 as a free-running counter reset at 0xFF without an IRQ; INT0 captures array data and alternates LEDs 6/7; KEY1 invokes the assembly sort.

## Concepts

polling/free-running timer; raw IRQ ownership; shared array; C-to-ASM call; LED state

## Constraints and risks

Timer1 reset match at 0xFF; no timer interrupt; C prototype must match ASM symbol and argument registers.

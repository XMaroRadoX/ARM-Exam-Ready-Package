# E2025-01-29-A3-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `board:dac`, `board:gpio`, `board:timer`, `risk:irq-shared-state`, `state:debounce`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM3.pdf`

## Requirement

Use Timer2 and KEY1/KEY2 to fill arrays, then use INT0 to verify the requested algebraic property and display pass/fail on LEDs.

## Concepts

two-button input; timer value capture; two arrays; IRQ event; verification; LED pass/fail

## Constraints and risks

Free-running Timer2 as specified; Assembly receives complete buffers and returns a defined Boolean/status.

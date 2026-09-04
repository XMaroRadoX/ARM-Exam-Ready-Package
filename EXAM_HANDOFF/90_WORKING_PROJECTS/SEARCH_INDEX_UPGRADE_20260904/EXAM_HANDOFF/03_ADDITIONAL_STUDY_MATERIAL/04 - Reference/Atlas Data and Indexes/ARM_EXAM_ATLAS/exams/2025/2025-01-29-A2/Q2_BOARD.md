# E2025-01-29-A2-Q2

- Delivery: `C + ASM call`
- Tags: `board:gpio`, `board:timer`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:irq-shared-state`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM2.pdf`

## Requirement

Use the specified free-running timer and interrupts to fill matrices A and B; invoke multiplication on KEY1; display result rows on LEDs every 0.5 seconds.

## Concepts

two input buffers; IRQ capture; C/ASM call; periodic LED row display

## Constraints and risks

0.5 s row display; paper-specific free-running timer; Do not expose partially filled buffers to ASM; use a ready flag or count.

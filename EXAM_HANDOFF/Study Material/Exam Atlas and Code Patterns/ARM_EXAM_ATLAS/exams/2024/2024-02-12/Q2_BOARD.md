# E2024-02-12-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `alg:graph-search`, `board:gpio`, `board:timer`, `cpu:flags`, `flow:nested-loop`, `mem:matrix-row-major`, `risk:irq-shared-state`, `state:debounce`, `state:event-loop`, `timing:free-running`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-CPU-FLAGS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-TIMER-FREE-RUNNING-001`
- Source: `Material (8)\Exams\23-24\20240212 arm.pdf`

## Requirement

Generate a random maze with an LCG seeded from a free-running Timer0, start from KEY2, fill the byte matrix safely, and call the assembly solver.

## Concepts

LCG; free-running timer seed; button event; nested C loops; C/ASM matrix contract

## Constraints and risks

Free-running Timer0 used as seed; Pass base pointer and dimensions in the agreed argument registers; define byte element type.

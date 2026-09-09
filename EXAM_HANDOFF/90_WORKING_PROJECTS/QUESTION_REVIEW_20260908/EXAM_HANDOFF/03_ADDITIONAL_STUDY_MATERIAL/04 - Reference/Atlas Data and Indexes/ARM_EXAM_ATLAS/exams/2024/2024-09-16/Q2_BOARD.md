# E2024-09-16-Q2

- Delivery: `C`
- Tags: `abi:nonleaf`, `board:gpio`, `cpu:flags`, `mem:matrix-row-major`, `risk:irq-shared-state`, `state:debounce`, `state:event-loop`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-GPIO-EVENT-001`, `PAT-CPU-FLAGS-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`
- Source: `Material (8)\Exams\23-24\20240916 arm.pdf`

## Requirement

Implement a two-button state machine that increments a value and applies the required offset while handling event order and button behavior.

## Concepts

two-button state machine; increment/offset; debouncing choice; event flags

## Constraints and risks

Button events; debounce according to requirement; N/A

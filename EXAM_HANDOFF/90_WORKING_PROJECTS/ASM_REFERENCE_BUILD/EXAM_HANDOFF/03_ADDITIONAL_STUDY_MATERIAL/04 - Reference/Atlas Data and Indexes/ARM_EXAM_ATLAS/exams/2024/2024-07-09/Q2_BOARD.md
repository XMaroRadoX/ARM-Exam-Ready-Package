# E2024-07-09-Q2

- Delivery: `ASM startup/exception`
- Tags: `abi:nonleaf`, `alg:graph-search`, `alg:recurrence`, `board:timer`, `risk:stack-alignment`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-RECURRENCE-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\23-24\20240709 arm.pdf`

## Requirement

Configure SysTick directly in Reset_Handler, collect available moves, choose one using modulo arithmetic, and keep the stack balanced across all branches.

## Concepts

startup code; raw SysTick; choice array/stack; modulo; balanced stack

## Constraints and risks

Direct reload/control configuration as specified by the paper; Reset context and handler ownership differ from ordinary C calls; every path must restore SP.

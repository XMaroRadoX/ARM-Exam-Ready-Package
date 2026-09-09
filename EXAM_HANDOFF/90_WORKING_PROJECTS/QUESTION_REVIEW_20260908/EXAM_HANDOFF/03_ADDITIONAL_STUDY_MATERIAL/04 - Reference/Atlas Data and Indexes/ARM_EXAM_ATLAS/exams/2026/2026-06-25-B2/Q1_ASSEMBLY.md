# E2026-06-25-B2-Q1

- Delivery: `ASM`
- Tags: `abi:four-register-args`, `alg:frequency-count`, `flow:early-break`, `flow:nested-loop`, `mem:word-array`, `risk:stack-alignment`, `timing:periodic`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Exams\Exam 25.06.2206\20260625_ARM_2.pdf`

## Requirement

Implement Mastermind over four word arrays, mark exact matches, find unmatched partial matches with a nested search and break, and return the encoded result.

## Concepts

four arrays; exact-match pass; nested search; used markers; break; encoded return

## Constraints and risks

N/A; Four pointers consume R0-R3; preserve outer-loop state and R4-R11; every early break must keep SP balanced.

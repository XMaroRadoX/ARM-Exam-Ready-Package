# E2023-07-04

- Date: `2023-07-04`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230704 arm.pdf`
- SHA-256: `00b04fb9ee48348d35f760dc4be463f251c7e107e6fece712f732e2ce8e0a82c`
- Answer collection: `Study Material/03 - Solved Exams/2023-07-04_Sociable_Timer`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:non-leaf`, `algorithm:aliquot-sum`, `algorithm:circular-sequence`, `algorithm:divisor-search`, `algorithm:recurrence`, `algorithm:sociable-sequence`, `data:word-array`, `event:timer-interrupt`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:led`, `peripheral:timer1`, `risk:division`, `risk:irq-shared-state`, `risk:stack-balance`, `risk:termination`, `risk:timer-ownership`, `timing:periodic-2-seconds`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-PRIME-FACTORIZATION-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Compute aliquot sums and detect a sociable-number sequence using divisor tests, nested loops and subroutine calls.

- Type: `assembly-algorithm`
- Algorithms: `aliquot-sum;sociable-sequence;divisor-search;recurrence`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;non-leaf;word-array`
- Risks: `termination;division;stack-balance`
- Search words: sociable numbers aliquot proper divisors cycle
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-PRIME-FACTORIZATION-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

Configure Timer1 for a two-second periodic event, advance a circular sequence array, call the assembly routine, and display the result on LEDs.

- Type: `c-board-integration`
- Algorithms: `circular-sequence`
- Peripherals/events/timing: `led;periodic-2-seconds;timer-interrupt;timer1`
- Data/ABI: `c-calls-assembly;word-array`
- Risks: `irq-shared-state;timer-ownership`
- Search words: periodic timer circular array display assembly call
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

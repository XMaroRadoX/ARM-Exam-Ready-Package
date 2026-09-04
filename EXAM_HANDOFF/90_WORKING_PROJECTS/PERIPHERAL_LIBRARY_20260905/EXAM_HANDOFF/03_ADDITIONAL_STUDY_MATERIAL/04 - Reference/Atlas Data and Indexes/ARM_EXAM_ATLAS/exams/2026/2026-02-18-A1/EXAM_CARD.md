# E2026-02-18-A1

- Date: `2026-02-18`
- Variant: `ARM1`
- Source PDF: `Exams/Exam 18.02.2026/20260218_ARM_1.pdf`
- SHA-256: `0ef4f9295c4d1d486e29a037ebdd0f159208e131d2fa26ce3723b223b0887fa2`
- Answer collection: `Study Material/03 - Solved Exams/2026-02-18_ARM1_Three_Timers`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:two-arguments`, `algorithm:duration-scaling`, `algorithm:frequency-scaling`, `algorithm:hofstadter-q`, `algorithm:indirect-recurrence`, `algorithm:maximum-reduction`, `algorithm:sample-streaming`, `data:sine-table-45`, `data:uint16-samples`, `data:word-array-1000`, `event:three-timer-interrupts`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:dac`, `peripheral:speaker`, `peripheral:timer-a`, `peripheral:timer-b`, `peripheral:timer-c`, `risk:bounds`, `risk:indirect-index`, `risk:irq-shared-state`, `risk:one-based-vs-zero-based`, `risk:overflow-order`, `risk:running-state`, `risk:sample-wrap`, `risk:stack-balance`, `risk:three-timer-ownership`, `timing:one-shot-duration`, `timing:periodic-sample-rate`, `timing:scheduler-50-ms`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-INDIRECT-RECURRENCE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-REDUCTION-001`, `PAT-ALG-SATURATING-ARITHMETIC-001`, `PAT-DAC-STREAM-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Questions

### Q1 - ASM

Generate the iterative Hofstadter Q sequence in a word array and return or track the required maximum while handling early indices safely.

- Type: `assembly-algorithm`
- Algorithms: `hofstadter-q;indirect-recurrence;maximum-reduction`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;two-arguments;word-array-1000`
- Risks: `one-based-vs-zero-based;indirect-index;bounds;stack-balance`
- Search words: Hofstadter Q iterative previous indexed terms maximum
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-INDIRECT-RECURRENCE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-REDUCTION-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

Coordinate three timers for A/B/C states, stream SinTable[45] through the DAC, use a 50 ms scheduler tick, compute frequency/duration values, and track whether each timer is running.

- Type: `c-board-integration`
- Algorithms: `frequency-scaling;duration-scaling;sample-streaming`
- Peripherals/events/timing: `dac;one-shot-duration;periodic-sample-rate;scheduler-50-ms;speaker;three-timer-interrupts;timer-a;timer-b;timer-c`
- Data/ABI: `c-calls-assembly;sine-table-45;uint16-samples;word-array-1000`
- Risks: `overflow-order;irq-shared-state;three-timer-ownership;sample-wrap;running-state`
- Search words: three timers Hofstadter music SinTable DAC speaker threshold frequency duration
- Pattern IDs: `PAT-ALG-SATURATING-ARITHMETIC-001`, `PAT-DAC-STREAM-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

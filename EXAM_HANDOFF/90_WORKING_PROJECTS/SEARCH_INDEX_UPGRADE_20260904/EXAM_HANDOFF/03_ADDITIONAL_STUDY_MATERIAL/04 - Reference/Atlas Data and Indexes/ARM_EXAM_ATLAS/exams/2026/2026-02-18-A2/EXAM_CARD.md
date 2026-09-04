# E2026-02-18-A2

- Date: `2026-02-18`
- Variant: `ARM2`
- Source PDF: `Exams/Exam 18.02.2026/20260218_ARM_2.pdf`
- SHA-256: `4dfecf2ee5556c9aa2b55184743e35fad063e50c0960233a80f5404312d458ea`
- Answer collection: `Study Material/03 - Solved Exams/2026-02-18_ARM2_Three_Timers`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:two-arguments`, `algorithm:duration-scaling`, `algorithm:frequency-scaling`, `algorithm:hofstadter-conway`, `algorithm:indirect-recurrence`, `algorithm:maximum-reduction`, `algorithm:sample-streaming`, `data:first-1000-used`, `data:sine-table-45`, `data:uint16-samples`, `data:word-array-1000`, `data:word-array-10000-declared`, `event:three-timer-interrupts`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:dac`, `peripheral:speaker`, `peripheral:timer-a`, `peripheral:timer-b`, `peripheral:timer-c`, `risk:bounds`, `risk:indirect-index`, `risk:irq-shared-state`, `risk:large-static-array`, `risk:one-based-vs-zero-based`, `risk:overflow-order`, `risk:running-state`, `risk:sample-wrap`, `risk:stack-balance`, `risk:three-timer-ownership`, `timing:one-shot-duration`, `timing:periodic-sample-rate`, `timing:scheduler-50-ms`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-INDIRECT-RECURRENCE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-REDUCTION-001`, `PAT-ALG-SATURATING-ARITHMETIC-001`, `PAT-DAC-STREAM-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Questions

### Q1 - ASM

Generate the Hofstadter-Conway variant iteratively in a word array with correct seeds, recurrence-derived indexes and requested aggregate/result.

- Type: `assembly-algorithm`
- Algorithms: `hofstadter-conway;indirect-recurrence;maximum-reduction`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;first-1000-used;two-arguments;word-array-10000-declared`
- Risks: `one-based-vs-zero-based;indirect-index;large-static-array;bounds;stack-balance`
- Search words: Hofstadter Conway 10000 iterative indirect indexes maximum large array
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-INDIRECT-RECURRENCE-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-REDUCTION-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

Implement the three-timer, DAC and 50 ms scheduling variant, including frequency/duration calculations and explicit running/stopped states.

- Type: `c-board-integration`
- Algorithms: `frequency-scaling;duration-scaling;sample-streaming`
- Peripherals/events/timing: `dac;one-shot-duration;periodic-sample-rate;scheduler-50-ms;speaker;three-timer-interrupts;timer-a;timer-b;timer-c`
- Data/ABI: `c-calls-assembly;sine-table-45;uint16-samples;word-array-1000`
- Risks: `overflow-order;irq-shared-state;three-timer-ownership;sample-wrap;running-state`
- Search words: three timers Hofstadter Conway music SinTable DAC speaker threshold
- Pattern IDs: `PAT-ALG-SATURATING-ARITHMETIC-001`, `PAT-DAC-STREAM-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

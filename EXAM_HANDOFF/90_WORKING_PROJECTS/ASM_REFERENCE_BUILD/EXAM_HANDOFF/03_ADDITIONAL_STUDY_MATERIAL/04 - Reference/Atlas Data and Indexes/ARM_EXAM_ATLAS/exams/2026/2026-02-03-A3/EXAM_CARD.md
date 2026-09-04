# E2026-02-03-A3

- Date: `2026-02-03`
- Variant: `ARM3`
- Source PDF: `Exams/Exam 03.02.2026/20260203_ARM_3.pdf`
- SHA-256: `3b7d7638803bf8e8c0329eca34265667b4df7ad4c19a500b45b0e1566074d46b`
- Answer collection: `Study Material/03 - Solved Exams/2026-02-03_ARM3_Recaman_ADC_Timer`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:non-leaf`, `algorithm:adc-display`, `algorithm:duplicate-search`, `algorithm:indirect-recurrence`, `algorithm:recaman`, `algorithm:sequence-display`, `data:adc-12-bit`, `data:word-array`, `event:adc-complete`, `event:key2`, `event:timer-interrupt`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:adc`, `peripheral:buttons`, `peripheral:led`, `peripheral:potentiometer`, `peripheral:timer`, `risk:adc-channel`, `risk:bounds`, `risk:debounce`, `risk:duplicate-detection`, `risk:irq-shared-state`, `risk:positive-subtraction`, `risk:stack-balance`, `risk:timer-ownership`, `timing:periodic-2-seconds`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-INDIRECT-RECURRENCE-001`, `PAT-ALG-LINEAR-SEARCH-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Fill a word array with the Recaman sequence, selecting subtraction only when positive and not already present, otherwise addition.

- Type: `assembly-algorithm`
- Algorithms: `recaman;indirect-recurrence;duplicate-search`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;non-leaf;word-array`
- Risks: `duplicate-detection;positive-subtraction;bounds;stack-balance`
- Search words: Recaman subtract if positive unused otherwise add
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-INDIRECT-RECURRENCE-001`, `PAT-ALG-LINEAR-SEARCH-001`, `PAT-ALG-RECURRENCE-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

Read/display ADC data, use KEY2 to generate the sequence, and use a two-second timer to display sequence values on LEDs.

- Type: `c-board-integration`
- Algorithms: `adc-display;sequence-display`
- Peripherals/events/timing: `adc;adc-complete;buttons;key2;led;periodic-2-seconds;potentiometer;timer;timer-interrupt`
- Data/ABI: `adc-12-bit;c-calls-assembly;word-array`
- Risks: `debounce;irq-shared-state;adc-channel;timer-ownership;bounds`
- Search words: ADC potentiometer KEY2 Recaman two second timer LEDs
- Pattern IDs: `PAT-ADC-SAMPLE-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

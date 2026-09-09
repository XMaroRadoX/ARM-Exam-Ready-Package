# E2023-09-18

- Date: `2023-09-18`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230918 arm.pdf`
- SHA-256: `2e6568d814b67ff734004e311accb982e610ba7544cdb5f1f91b324981b7846b`
- Answer collection: `Study Material/03 - Solved Exams/2023-09-18_DigitAddition_Buttons`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:non-leaf`, `algorithm:array-comparison`, `algorithm:binary-value-construction`, `algorithm:decimal-digits`, `algorithm:digit-addition`, `algorithm:digit-sum`, `data:digit-array`, `data:scalar`, `data:word-array`, `event:int0`, `event:key1`, `event:key2`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:led`, `risk:arithmetic-overflow`, `risk:debounce`, `risk:irq-shared-state`, `risk:stack-balance`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-DECIMAL-DIGITS-001`, `PAT-CPU-FLAGS-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Questions

### Q1 - ASM

Implement digitSum and digitaddition so one assembly subroutine calls another and reports arithmetic overflow correctly.

- Type: `assembly-algorithm`
- Algorithms: `digit-sum;digit-addition;decimal-digits`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;digit-array;non-leaf;scalar`
- Risks: `arithmetic-overflow;stack-balance`
- Search words: digitSum digitaddition decimal carry overflow nested BL
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-DECIMAL-DIGITS-001`, `PAT-CPU-FLAGS-001`

### Q2 - C + ASM call

Use KEY1 and KEY2 to build a binary value K, trigger processing from INT0, manage arrays, call assembly and show the comparison result on LEDs.

- Type: `c-board-integration`
- Algorithms: `binary-value-construction;array-comparison`
- Peripherals/events/timing: `buttons;int0;key1;key2;led`
- Data/ABI: `c-calls-assembly;word-array`
- Risks: `debounce;irq-shared-state`
- Search words: KEY1 KEY2 INT0 binary K arrays compare LEDs
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

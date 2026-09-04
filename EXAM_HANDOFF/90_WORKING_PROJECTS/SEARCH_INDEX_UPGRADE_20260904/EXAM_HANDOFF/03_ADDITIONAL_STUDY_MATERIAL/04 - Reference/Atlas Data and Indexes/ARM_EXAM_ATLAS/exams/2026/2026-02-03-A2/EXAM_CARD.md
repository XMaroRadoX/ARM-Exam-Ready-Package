# E2026-02-03-A2

- Date: `2026-02-03`
- Variant: `ARM2`
- Source PDF: `Exams/Exam 03.02.2026/20260203_ARM_2.pdf`
- SHA-256: `ecc909cda345d5f4bbd6c6978f0417a8921c5647290b8feaadba497438a44829`
- Answer collection: `Study Material/03 - Solved Exams/2026-02-03_ARM2_RLE_ADC`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `algorithm:adc-display`, `algorithm:run-grouping`, `algorithm:run-length-encoding`, `data:adc-12-bit`, `data:byte-array`, `data:count-value-output`, `data:digit-byte-array`, `event:adc-complete`, `event:key1`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:adc`, `peripheral:buttons`, `peripheral:led`, `peripheral:potentiometer`, `risk:adc-channel`, `risk:bounds`, `risk:capacity`, `risk:debounce`, `risk:final-run`, `risk:irq-shared-state`, `risk:stack-balance`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-RUN-LENGTH-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Questions

### Q1 - ASM

Run-length encode the digit array into the required count/value format, including final-run handling and output length.

- Type: `assembly-algorithm`
- Algorithms: `run-length-encoding;run-grouping`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;count-value-output;digit-byte-array`
- Risks: `capacity;final-run;bounds;stack-balance`
- Search words: RLE run length encoding final run output length
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-RUN-LENGTH-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-MEM-BYTE-ARRAY-001`

### Q2 - C + ASM call

Read the potentiometer with ADC, show its high eight bits on LEDs, and invoke the encoder from KEY1 with the required debounce behavior.

- Type: `c-board-integration`
- Algorithms: `adc-display;run-length-encoding`
- Peripherals/events/timing: `adc;adc-complete;buttons;key1;led;potentiometer`
- Data/ABI: `adc-12-bit;byte-array;c-calls-assembly`
- Risks: `debounce;irq-shared-state;adc-channel;bounds`
- Search words: potentiometer ADC channel 5 high eight bits KEY1 RLE
- Pattern IDs: `PAT-ADC-SAMPLE-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

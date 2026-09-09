# E2026-02-03-A1

- Date: `2026-02-03`
- Variant: `ARM1`
- Source PDF: `Exams/Exam 03.02.2026/20260203_ARM_1.pdf`
- SHA-256: `4d1f2a9349357a96f0785b83bf347553e73bcd551ccac6d4086dbe5a545488f4`
- Answer collection: `Study Material/03 - Solved Exams/2026-02-03_ARM1_LookAndSay_ADC`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:non-leaf`, `algorithm:adc-display`, `algorithm:bounded-output`, `algorithm:look-and-say`, `algorithm:run-grouping`, `algorithm:sequence-generation`, `data:adc-12-bit`, `data:byte-array`, `data:digit-byte-array`, `data:output-buffer`, `event:adc-complete`, `event:int0`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:adc`, `peripheral:buttons`, `peripheral:led`, `peripheral:potentiometer`, `risk:adc-channel`, `risk:bounds`, `risk:capacity`, `risk:debounce`, `risk:final-run`, `risk:irq-shared-state`, `risk:stack-balance`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-LOOK-AND-SAY-001`, `PAT-ALG-RUN-LENGTH-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Questions

### Q1 - ASM

Generate the Look-and-Say sequence in the required digit representation, grouping equal runs and writing count/value pairs without overrunning the output buffer.

- Type: `assembly-algorithm`
- Algorithms: `look-and-say;run-grouping;bounded-output`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;digit-byte-array;non-leaf;output-buffer`
- Risks: `capacity;final-run;bounds;stack-balance`
- Search words: Look-and-Say count value pairs output capacity digits
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-LOOK-AND-SAY-001`, `PAT-ALG-RUN-LENGTH-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`

### Q2 - C + ASM call

Read the potentiometer through ADC, show the top eight bits on LEDs, and on INT0 call the assembly routine with physical debouncing enabled.

- Type: `c-board-integration`
- Algorithms: `adc-display;sequence-generation`
- Peripherals/events/timing: `adc;adc-complete;buttons;int0;led;potentiometer`
- Data/ABI: `adc-12-bit;byte-array;c-calls-assembly`
- Risks: `debounce;irq-shared-state;adc-channel;bounds`
- Search words: potentiometer ADC channel 5 high eight bits INT0 look say
- Pattern IDs: `PAT-ADC-SAMPLE-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

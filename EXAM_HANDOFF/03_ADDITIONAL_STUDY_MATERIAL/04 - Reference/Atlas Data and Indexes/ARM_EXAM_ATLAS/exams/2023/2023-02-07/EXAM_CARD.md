# E2023-02-07

- Date: `2023-02-07`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230207 arm.pdf`
- SHA-256: `77929b413afda671274838630078b32bbebe1e643e1102a00412a7209879ce26`
- Answer collection: `Study Material/03 - Solved Exams/2023-02-07_Sort_FreeRunning_Timer`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:non-leaf`, `algorithm:array-copy`, `algorithm:capture-and-sort`, `algorithm:insertion-sort`, `data:read-only-input`, `data:signed-byte-array`, `data:writable-output`, `event:int0`, `event:key1`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:led`, `peripheral:timer1`, `risk:bounds`, `risk:debounce`, `risk:irq-shared-state`, `risk:signedness`, `risk:stack-balance`, `risk:timer-ownership`, `risk:vector-ownership`, `timing:free-running`, `timing:reset-at-match-no-irq`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-SORTING-001`, `PAT-DATA-ASM-OBJECTS-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Questions

### Q1 - ASM

Copy signed byte values into a working array, then perform insertion sort while preserving signed ordering and array bounds.

- Type: `assembly-algorithm`
- Algorithms: `array-copy;insertion-sort`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;non-leaf;read-only-input;signed-byte-array;writable-output`
- Risks: `signedness;bounds;stack-balance`
- Search words: sort signed bytes copy array insertion stable
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-SORTING-001`, `PAT-DATA-ASM-OBJECTS-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`

### Q2 - C + ASM call

Use Timer1 as a free-running counter reset at 0xFF without an IRQ; INT0 captures array data and alternates LEDs 6/7; KEY1 invokes the assembly sort.

- Type: `c-board-integration`
- Algorithms: `capture-and-sort`
- Peripherals/events/timing: `buttons;free-running;int0;key1;led;reset-at-match-no-irq;timer1`
- Data/ABI: `c-calls-assembly;signed-byte-array`
- Risks: `debounce;irq-shared-state;timer-ownership;vector-ownership`
- Search words: timer seed counter 0xff LED6 LED7 external interrupt sort
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

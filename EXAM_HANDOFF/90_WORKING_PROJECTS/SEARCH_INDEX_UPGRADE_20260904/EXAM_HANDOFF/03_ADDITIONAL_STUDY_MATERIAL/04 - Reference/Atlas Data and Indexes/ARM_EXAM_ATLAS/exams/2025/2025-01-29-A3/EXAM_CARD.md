# E2025-01-29-A3

- Date: `2025-01-29`
- Variant: `ARM3`
- Source PDF: `Exams/24-25/2025_01_29/20250129_ARM3.pdf`
- SHA-256: `761ce33d98721985812e9dac30fedd846893bfc2ccbc7b16513615d24cde2a6e`
- Answer collection: `Study Material/03 - Solved Exams/2025-01-29_ARM3_Transpose_Timer`
- Search tags: `abi:c-calls-assembly-three-times`, `abi:callee-saved-registers`, `abi:two-pointer-arguments`, `algorithm:array-capture`, `algorithm:packed-matrix-transpose`, `algorithm:xor-equivalence`, `data:byte-array`, `data:five-byte-arrays`, `data:packed-8x8-bit-matrices`, `data:packed-8x8-bit-matrix`, `data:read-only-input`, `data:writable-output`, `event:int0`, `event:key1`, `event:key2`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:led`, `peripheral:timer2`, `risk:bounds`, `risk:debounce`, `risk:irq-shared-state`, `risk:msb-first-bit-order`, `risk:stack-balance`, `risk:timer-ownership`, `timing:free-running-reset-at-0xffff-no-irq`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-DATA-ASM-OBJECTS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-PACKED-TRANSPOSE-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Questions

### Q1 - ASM

Transpose a packed binary matrix by exchanging row/column bit coordinates without corrupting unrelated bits.

- Type: `assembly-algorithm`
- Algorithms: `packed-matrix-transpose`
- Peripherals/events/timing: `none`
- Data/ABI: `byte-array;callee-saved-registers;packed-8x8-bit-matrix;read-only-input;two-pointer-arguments;writable-output`
- Risks: `msb-first-bit-order;bounds;stack-balance`
- Search words: transpose AT bit matrix 8 bytes DCB READONLY READWRITE
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-DATA-ASM-OBJECTS-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-PACKED-TRANSPOSE-001`

### Q2 - C + ASM call

Use Timer2 and KEY1/KEY2 to fill arrays, then use INT0 to verify the requested algebraic property and display pass/fail on LEDs.

- Type: `c-board-integration`
- Algorithms: `array-capture;xor-equivalence`
- Peripherals/events/timing: `buttons;free-running-reset-at-0xffff-no-irq;int0;key1;key2;led;timer2`
- Data/ABI: `c-calls-assembly-three-times;five-byte-arrays;packed-8x8-bit-matrices`
- Risks: `debounce;bounds;irq-shared-state;timer-ownership`
- Search words: A XOR B transpose equivalence Timer2 arrays LEDs 4 5
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-PACKED-TRANSPOSE-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

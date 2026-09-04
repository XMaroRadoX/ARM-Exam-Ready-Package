# E2025-01-29-A1

- Date: `2025-01-29`
- Variant: `ARM1`
- Source PDF: `Exams/24-25/2025_01_29/20250129_ARM1.pdf`
- SHA-256: `81b1160be1d5b7aa4520486427166188d838607a3f22089c7b04734b3dad4575`
- Answer collection: `Study Material/03 - Solved Exams/2025-01-29_ARM1_Affine_Two_Timers`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `algorithm:bitwise-affine-transform`, `algorithm:byte-capture`, `algorithm:packed-matrix`, `algorithm:row-display`, `algorithm:xor`, `data:byte-array`, `data:packed-8x8-bit-matrix`, `event:int0`, `event:key1`, `event:timer0-interrupt`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:led`, `peripheral:timer0`, `peripheral:timer1`, `risk:bit-order`, `risk:bounds`, `risk:debounce`, `risk:irq-shared-state`, `risk:row-order`, `risk:stack-balance`, `risk:timer-ownership`, `timing:free-running`, `timing:periodic-500-ms-full-cycle`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Apply the requested bitwise affine transformation to a packed 8x8 binary matrix while preserving the specified bit and row order.

- Type: `assembly-algorithm`
- Algorithms: `bitwise-affine-transform;packed-matrix`
- Peripherals/events/timing: `none`
- Data/ABI: `byte-array;callee-saved-registers;packed-8x8-bit-matrix`
- Risks: `bit-order;row-order;bounds;stack-balance`
- Search words: affine bit matrix packed 8x8 masks shifts
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`

### Q2 - C + ASM call

Run Timer1 freely with reset at 0xFFFF and no IRQ; INT0 collects bytes and XORs/displays them; KEY1 calls the assembly transform; Timer0 blinks rows with a 0.5-second full period.

- Type: `c-board-integration`
- Algorithms: `byte-capture;xor;row-display`
- Peripherals/events/timing: `buttons;free-running;int0;key1;led;periodic-500-ms-full-cycle;timer0;timer0-interrupt;timer1`
- Data/ABI: `byte-array;c-calls-assembly;packed-8x8-bit-matrix`
- Risks: `debounce;irq-shared-state;timer-ownership`
- Search words: Timer1 0xffff free counter Timer0 blink rows XOR INT0 KEY1
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

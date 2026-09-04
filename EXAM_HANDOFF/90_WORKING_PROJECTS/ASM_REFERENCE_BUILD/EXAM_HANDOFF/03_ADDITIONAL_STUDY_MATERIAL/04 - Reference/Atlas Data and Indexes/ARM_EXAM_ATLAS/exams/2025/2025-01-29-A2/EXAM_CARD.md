# E2025-01-29-A2

- Date: `2025-01-29`
- Variant: `ARM2`
- Source PDF: `Exams/24-25/2025_01_29/20250129_ARM2.pdf`
- SHA-256: `af077d82dca1acfbbac322ee1774a4d6c4ec796d42721c073e0b0fc20543e50b`
- Answer collection: `Study Material/03 - Solved Exams/2025-01-29_ARM2_Matrix_Two_Timers`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `algorithm:binary-matrix-multiplication`, `algorithm:bit-dot-product`, `algorithm:matrix-capture`, `algorithm:row-display`, `data:byte-array`, `data:output-matrix`, `data:packed-8x8-bit-matrix`, `data:two-packed-matrices`, `event:int0`, `event:key1`, `event:timer0-interrupt`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:led`, `peripheral:timer0`, `peripheral:timer1`, `risk:bit-order`, `risk:bounds`, `risk:debounce`, `risk:irq-shared-state`, `risk:stack-balance`, `risk:timer-ownership`, `timing:free-running`, `timing:periodic-500-ms`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-ALG-PACKED-MATMUL-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Multiply two packed binary matrices using bit-level dot products and store the packed result with the required orientation.

- Type: `assembly-algorithm`
- Algorithms: `binary-matrix-multiplication;bit-dot-product`
- Peripherals/events/timing: `none`
- Data/ABI: `byte-array;callee-saved-registers;packed-8x8-bit-matrix`
- Risks: `bit-order;bounds;stack-balance`
- Search words: packed binary matrix multiplication GF2 bit dot product
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-ALG-PACKED-MATMUL-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`

### Q2 - C + ASM call

Use the specified free-running timer and interrupts to fill matrices A and B; invoke multiplication on KEY1; display result rows on LEDs every 0.5 seconds.

- Type: `c-board-integration`
- Algorithms: `matrix-capture;row-display`
- Peripherals/events/timing: `buttons;free-running;int0;key1;led;periodic-500-ms;timer0;timer0-interrupt;timer1`
- Data/ABI: `c-calls-assembly;output-matrix;two-packed-matrices`
- Risks: `debounce;irq-shared-state;timer-ownership`
- Search words: fill matrices A B free timer multiply display rows
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

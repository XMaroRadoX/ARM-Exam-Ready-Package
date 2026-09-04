# E2025-02-12-A2

- Date: `2025-02-12`
- Variant: `ARM2`
- Source PDF: `Exams/24-25/2025_02_12/20250212_ARM2.pdf`
- SHA-256: `6260e7e253a7ddd3c5e186b84f08ef3366e0f4d062501001dadd1abb872a8b10`
- Answer collection: `Study Material/03 - Solved Exams/2025-02-12_ARM2_Cosine_DAC`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:non-leaf`, `algorithm:cosine-maclaurin`, `algorithm:fixed-point-recurrence`, `algorithm:sample-streaming`, `algorithm:waveform-generation`, `data:cosine-table`, `data:sample-table`, `data:signed-word-array`, `event:key1`, `event:timer1-interrupt`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:dac`, `peripheral:speaker`, `peripheral:timer1`, `risk:bounds`, `risk:debounce`, `risk:fixed-point-scale`, `risk:irq-shared-state`, `risk:overflow`, `risk:sample-bounds`, `risk:signedness`, `risk:stack-balance`, `risk:timer-ownership`, `timing:periodic-1592-cycles`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Generate cosine values with the required fixed-point recurrence, scale and array bounds.

- Type: `assembly-algorithm`
- Algorithms: `cosine-maclaurin;fixed-point-recurrence`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;non-leaf;sample-table;signed-word-array`
- Risks: `fixed-point-scale;signedness;overflow;bounds;stack-balance`
- Search words: cosine Maclaurin fixed point recurrence samples
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

Use KEY1 to generate the waveform, configure Timer1 every 1592 cycles, and stream the table through the DAC according to the stated trigger behavior.

- Type: `c-board-integration`
- Algorithms: `waveform-generation;sample-streaming`
- Peripherals/events/timing: `buttons;dac;key1;periodic-1592-cycles;speaker;timer1;timer1-interrupt`
- Data/ABI: `c-calls-assembly;cosine-table`
- Risks: `debounce;irq-shared-state;timer-ownership;sample-bounds`
- Search words: KEY1 Timer1 1592 cycles DAC cosine waveform
- Pattern IDs: `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

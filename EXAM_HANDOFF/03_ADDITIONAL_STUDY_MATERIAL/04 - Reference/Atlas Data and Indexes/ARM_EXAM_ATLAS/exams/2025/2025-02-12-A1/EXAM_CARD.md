# E2025-02-12-A1

- Date: `2025-02-12`
- Variant: `ARM1`
- Source PDF: `Exams/24-25/2025_02_12/20250212_ARM1.pdf`
- SHA-256: `04bdc71658fd0d480ff738ea259fb791ea48991a1e45b2f4d8ec082de65a597f`
- Answer collection: `Study Material/03 - Solved Exams/2025-02-12_ARM1_Sine_DAC`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:non-leaf`, `algorithm:fixed-point-recurrence`, `algorithm:sample-streaming`, `algorithm:sine-maclaurin`, `algorithm:waveform-generation`, `data:sample-table`, `data:signed-word-array`, `data:sine-table-45`, `event:int0`, `event:timer0-interrupt`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:dac`, `peripheral:speaker`, `peripheral:timer0`, `risk:bounds`, `risk:fixed-point-scale`, `risk:irq-shared-state`, `risk:overflow`, `risk:sample-bounds`, `risk:signedness`, `risk:stack-balance`, `risk:timer-ownership`, `timing:periodic-1263-cycles`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Generate sine values with the stated Maclaurin/fixed-point recurrence, maintaining scale, signs, loop limits and array storage.

- Type: `assembly-algorithm`
- Algorithms: `sine-maclaurin;fixed-point-recurrence`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;non-leaf;sample-table;signed-word-array`
- Risks: `fixed-point-scale;signedness;overflow;bounds;stack-balance`
- Search words: sine Maclaurin fixed point recurrence 45 samples
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FIXED-POINT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

On INT0, call the assembly generator for sineValues[45]; configure Timer0 every 1263 cycles and stream the samples to the DAC; no debouncing is required.

- Type: `c-board-integration`
- Algorithms: `waveform-generation;sample-streaming`
- Peripherals/events/timing: `buttons;dac;int0;periodic-1263-cycles;speaker;timer0;timer0-interrupt`
- Data/ABI: `c-calls-assembly;sine-table-45`
- Risks: `irq-shared-state;timer-ownership;sample-bounds`
- Search words: INT0 no debounce Timer0 1263 cycles DAC sineValues 45
- Pattern IDs: `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

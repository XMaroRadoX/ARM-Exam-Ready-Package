# E2025-07-01-A2

- Date: `2025-07-01`
- Variant: `ARM2`
- Source PDF: `Exams/24-25/2025_07_01/ARM2.pdf`
- SHA-256: `61b5bc6866d95a1ce17fd0356cb661d342641945037f71924afc4050cfba1e81`
- Answer collection: `Study Material/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm`
- Search tags: `abi:callback`, `abi:callee-saved-registers`, `abi:five-arguments`, `abi:non-leaf`, `abi:reset-handler`, `abi:stacked-argument`, `algorithm:first-input-only`, `algorithm:lcg-sequence`, `algorithm:linear-congruential-generator`, `algorithm:modulo`, `algorithm:recurrence`, `algorithm:rhythm-game`, `algorithm:shift`, `data:persistent-state`, `data:unsigned-word-state`, `data:word-array`, `event:joystick-first-movement`, `event:timer1-interrupt`, `lang:assembly`, `lang:c`, `peripheral:joystick`, `peripheral:led`, `peripheral:timer1`, `risk:debounce`, `risk:first-event-latching`, `risk:irq-shared-state`, `risk:non-returning-loop`, `risk:shift-range`, `risk:stack-alignment`, `risk:stack-balance`, `risk:stacked-arguments`, `risk:stacked-offset`, `risk:timer-ownership`, `risk:unsigned-wrap`, `timing:periodic-2.5-seconds`, `type:assembly-algorithm`, `type:assembly-startup`, `type:c-board-state-machine`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-BITFIELD-001`, `PAT-ALG-LCG-001`, `PAT-ALG-RECURRENCE-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Implement the variant LCG with its shift operation and five-argument interface, preserving the specified arithmetic order.

- Type: `assembly-algorithm`
- Algorithms: `linear-congruential-generator;modulo;shift`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;five-arguments;stacked-argument;unsigned-word-state`
- Risks: `unsigned-wrap;shift-range;stacked-offset;stack-balance`
- Search words: LCG shift five parameters modulo unsigned
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-BITFIELD-001`, `PAT-ALG-LCG-001`

### Q2 - ASM startup

Drive the variant generator from Reset_Handler with correct argument construction and persistent loop state.

- Type: `assembly-startup`
- Algorithms: `lcg-sequence;recurrence;shift`
- Peripherals/events/timing: `none`
- Data/ABI: `five-arguments;non-leaf;persistent-state;reset-handler;word-array`
- Risks: `stack-alignment;stacked-arguments;non-returning-loop`
- Search words: Reset_Handler LCG shifted sequence startup
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-LCG-001`, `PAT-ALG-RECURRENCE-001`, `PAT-MEM-WORD-ARRAY-001`

### Q3 - C

Use Timer1 for a 2.5-second LED sequence and process only the joystick's first movement in the game logic.

- Type: `c-board-state-machine`
- Algorithms: `rhythm-game;first-input-only`
- Peripherals/events/timing: `joystick;joystick-first-movement;led;periodic-2.5-seconds;timer1;timer1-interrupt`
- Data/ABI: `callback`
- Risks: `debounce;first-event-latching;irq-shared-state;timer-ownership`
- Search words: rhythm game first joystick movement Timer1 2.5 seconds
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

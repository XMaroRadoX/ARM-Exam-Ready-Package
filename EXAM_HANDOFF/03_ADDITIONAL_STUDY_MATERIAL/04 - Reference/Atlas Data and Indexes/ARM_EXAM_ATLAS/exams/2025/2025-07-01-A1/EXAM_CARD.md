# E2025-07-01-A1

- Date: `2025-07-01`
- Variant: `ARM1`
- Source PDF: `Exams/24-25/2025_07_01/ARM1.pdf`
- SHA-256: `62e6a6f5101df35128b299c565c82f3338a8474dfb83b30e87efb2916a401843`
- Answer collection: `Study Material/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm`
- Search tags: `abi:callback`, `abi:callee-saved-registers`, `abi:five-arguments`, `abi:non-leaf`, `abi:reset-handler`, `abi:stacked-argument`, `algorithm:first-input-only`, `algorithm:lcg-sequence`, `algorithm:linear-congruential-generator`, `algorithm:modulo`, `algorithm:recurrence`, `algorithm:rhythm-game`, `data:persistent-state`, `data:unsigned-word-state`, `data:word-array`, `event:joystick-first-movement`, `event:timer0-interrupt`, `lang:assembly`, `lang:c`, `peripheral:joystick`, `peripheral:led`, `peripheral:timer0`, `risk:debounce`, `risk:divide-by-zero`, `risk:first-event-latching`, `risk:irq-shared-state`, `risk:non-returning-loop`, `risk:stack-alignment`, `risk:stack-balance`, `risk:stacked-arguments`, `risk:stacked-offset`, `risk:timer-ownership`, `risk:unsigned-wrap`, `timing:periodic-3-seconds`, `type:assembly-algorithm`, `type:assembly-startup`, `type:c-board-state-machine`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-LCG-001`, `PAT-ALG-RECURRENCE-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Implement the requested linear congruential generator with five parameters and correct unsigned wraparound/modulo behavior.

- Type: `assembly-algorithm`
- Algorithms: `linear-congruential-generator;modulo`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;five-arguments;stacked-argument;unsigned-word-state`
- Risks: `unsigned-wrap;divide-by-zero;stacked-offset;stack-balance`
- Search words: LCG five parameters modulo unsigned wrap
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-LCG-001`

### Q2 - ASM startup

Call the LCG repeatedly from Reset_Handler and maintain the required sequence/state without violating startup or call conventions.

- Type: `assembly-startup`
- Algorithms: `lcg-sequence;recurrence`
- Peripherals/events/timing: `none`
- Data/ABI: `five-arguments;non-leaf;persistent-state;reset-handler;word-array`
- Risks: `stack-alignment;stacked-arguments;non-returning-loop`
- Search words: Reset_Handler call LCG sequence startup persistent
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-LCG-001`, `PAT-ALG-RECURRENCE-001`, `PAT-MEM-WORD-ARRAY-001`

### Q3 - C

Use Timer0 for a three-second LED sequence and accept only the joystick's first movement for the rhythm-game state transition.

- Type: `c-board-state-machine`
- Algorithms: `rhythm-game;first-input-only`
- Peripherals/events/timing: `joystick;joystick-first-movement;led;periodic-3-seconds;timer0;timer0-interrupt`
- Data/ABI: `callback`
- Risks: `debounce;first-event-latching;irq-shared-state;timer-ownership`
- Search words: rhythm game first joystick movement Timer0 three seconds
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

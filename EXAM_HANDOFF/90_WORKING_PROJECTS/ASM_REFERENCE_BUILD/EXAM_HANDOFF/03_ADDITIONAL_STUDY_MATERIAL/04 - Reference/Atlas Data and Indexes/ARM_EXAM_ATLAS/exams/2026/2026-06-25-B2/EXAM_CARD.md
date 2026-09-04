# E2026-06-25-B2

- Date: `2026-06-25`
- Variant: `ARM2`
- Source PDF: `Exams/Exam 25.06.2206/20260625_ARM_2.pdf`
- SHA-256: `b643106147d4a20efe44ea7d6d39f1ec8dfc44d76d1625114779893efacb7124`
- Answer collection: `Study Material/03 - Solved Exams/2026-06-25_ARM2_Mastermind`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:four-register-arguments`, `algorithm:bitfield-display`, `algorithm:consume-once-matching`, `algorithm:early-break`, `algorithm:game-state-machine`, `algorithm:mastermind`, `algorithm:nested-search`, `algorithm:timer-derived-secret`, `data:four-two-bit-fields`, `data:four-word-arrays`, `data:used-marker-arrays`, `event:joystick-directions`, `event:joystick-select`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:joystick`, `peripheral:led`, `peripheral:timer`, `risk:debounce`, `risk:duplicates`, `risk:irq-shared-state`, `risk:operator-precedence`, `risk:secret-lifetime`, `risk:stack-balance`, `risk:state-transition`, `risk:timer-ownership`, `risk:zero-initialization`, `timing:free-running-seed`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-ALG-CONSUME-ONCE-MATCH-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Questions

### Q1 - ASM

Implement Mastermind over four word arrays, mark exact matches, find unmatched partial matches with a nested search and break, and return the encoded result.

- Type: `assembly-algorithm`
- Algorithms: `mastermind;consume-once-matching;nested-search;early-break`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;four-register-arguments;four-word-arrays;used-marker-arrays`
- Risks: `duplicates;zero-initialization;operator-precedence;stack-balance`
- Search words: Mastermind exact partial usedGuess usedSecret duplicate break encoded
- Pattern IDs: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-CONSUME-ONCE-MATCH-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

Build the corresponding debounced joystick-driven Mastermind game with timer-derived secret, per-digit LED fields, repeated guesses and encoded result display.

- Type: `c-board-integration`
- Algorithms: `game-state-machine;timer-derived-secret;bitfield-display`
- Peripherals/events/timing: `free-running-seed;joystick;joystick-directions;joystick-select;led;timer`
- Data/ABI: `c-calls-assembly;four-two-bit-fields;four-word-arrays`
- Risks: `debounce;secret-lifetime;state-transition;irq-shared-state;timer-ownership`
- Search words: Mastermind joystick select guess secret timer hexadecimal digits LEDs
- Pattern IDs: `PAT-ALG-BITFIELD-001`, `PAT-ALG-CONSUME-ONCE-MATCH-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

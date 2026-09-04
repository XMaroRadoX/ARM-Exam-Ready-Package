# E2026-06-25-B1

- Date: `2026-06-25`
- Variant: `ARM1`
- Source PDF: `Exams/Exam 25.06.2206/20260625_ARM_1.pdf`
- SHA-256: `a3f7eaca07f96a281382237948255abc1fadcfd2a3502d2e4d604921128fa2a8`
- Answer collection: `Study Material/03 - Solved Exams/2026-06-25_ARM1_BullsAndCows`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `abi:four-register-arguments`, `algorithm:bitfield-display`, `algorithm:bulls-and-cows`, `algorithm:duplicate-safe-matching`, `algorithm:frequency-count`, `algorithm:game-state-machine`, `algorithm:min-reduction`, `algorithm:timer-derived-secret`, `data:four-digits`, `data:four-two-bit-fields`, `data:four-word-arrays`, `event:joystick-directions`, `event:joystick-select`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:joystick`, `peripheral:led`, `peripheral:timer`, `risk:debounce`, `risk:duplicates`, `risk:irq-shared-state`, `risk:operator-precedence`, `risk:secret-lifetime`, `risk:stack-balance`, `risk:state-transition`, `risk:timer-ownership`, `risk:zero-initialization`, `timing:free-running-seed`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-BITFIELD-001`, `PAT-ALG-CONSUME-ONCE-MATCH-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ALG-REDUCTION-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Questions

### Q1 - ASM

Implement BullsAndCows over four word arrays, count exact matches and frequency-based partial matches, and return the encoded result.

- Type: `assembly-algorithm`
- Algorithms: `bulls-and-cows;frequency-count;duplicate-safe-matching;min-reduction`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;four-digits;four-register-arguments;four-word-arrays`
- Risks: `duplicates;zero-initialization;operator-precedence;stack-balance`
- Search words: BullsAndCows frequency arrays bulls cows duplicate digits encoded result
- Pattern IDs: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-CONSUME-ONCE-MATCH-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ALG-REDUCTION-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C + ASM call

Build a debounced joystick-driven Bulls and Cows game, seed a four-digit secret from a free-running timer, show the guess and encoded result on LEDs, and retain the secret across guesses.

- Type: `c-board-integration`
- Algorithms: `game-state-machine;timer-derived-secret;bitfield-display`
- Peripherals/events/timing: `free-running-seed;joystick;joystick-directions;joystick-select;led;timer`
- Data/ABI: `c-calls-assembly;four-two-bit-fields;four-word-arrays`
- Risks: `debounce;secret-lifetime;state-transition;irq-shared-state;timer-ownership`
- Search words: Bulls and Cows joystick select guess secret timer hexadecimal digits LEDs
- Pattern IDs: `PAT-ALG-BITFIELD-001`, `PAT-ALG-CONSUME-ONCE-MATCH-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

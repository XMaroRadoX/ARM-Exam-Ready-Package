# E2024-02-12

- Date: `2024-02-12`
- Variant: `ARM`
- Source PDF: `Exams/23-24/20240212 arm.pdf`
- SHA-256: `857211aa08989b7cd8e4630443c80fe33a4ad8e94d34a17636626deac8230ede`
- Answer collection: `Study Material/03 - Solved Exams/2024-02-12_Maze_LCG_Timer`
- Search tags: `abi:c-calls-assembly`, `abi:callee-saved-registers`, `algorithm:flood-fill`, `algorithm:graph-search`, `algorithm:lcg`, `algorithm:maze-generation`, `algorithm:maze-propagation`, `data:byte-matrix`, `data:row-major`, `event:key2`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:led`, `peripheral:timer0`, `risk:bounds`, `risk:debounce`, `risk:irq-shared-state`, `risk:no-progress-termination`, `risk:stack-balance`, `risk:timer-ownership`, `timing:free-running-seed`, `type:assembly-algorithm`, `type:c-board-integration`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FLOOD-FILL-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-LCG-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Questions

### Q1 - ASM

Solve a two-dimensional byte maze by repeatedly propagating reachable distances until the destination is reached or no progress remains.

- Type: `assembly-algorithm`
- Algorithms: `maze-propagation;flood-fill;graph-search`
- Peripherals/events/timing: `none`
- Data/ABI: `byte-matrix;callee-saved-registers;row-major`
- Risks: `bounds;no-progress-termination;stack-balance`
- Search words: maze wavefront propagation reachable distance walls destination
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FLOOD-FILL-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-FLOW-EARLY-BREAK-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`

### Q2 - C + ASM call

Generate a random maze with an LCG seeded from a free-running Timer0, start from KEY2, fill the byte matrix safely, and call the assembly solver.

- Type: `c-board-integration`
- Algorithms: `lcg;maze-generation`
- Peripherals/events/timing: `buttons;free-running-seed;key2;led;timer0`
- Data/ABI: `byte-matrix;c-calls-assembly;row-major`
- Risks: `debounce;bounds;irq-shared-state;timer-ownership`
- Search words: random maze LCG Timer0 seed KEY2 matrix solver
- Pattern IDs: `PAT-ALG-LCG-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

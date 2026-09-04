# E2024-02-28

- Date: `2024-02-28`
- Variant: `ARM`
- Source PDF: `Exams/23-24/20240228 arm.pdf`
- SHA-256: `772f6c10718ce63a360fd71027fbfce97bacac7b86829e48cf4bd3763d966783`
- Answer collection: `Study Material/03 - Solved Exams/2024-02-28_ShortestPath_Timer`
- Search tags: `abi:callback`, `abi:callee-saved-registers`, `algorithm:led-sequence`, `algorithm:maze-propagation`, `algorithm:unweighted-shortest-path`, `data:byte-matrix`, `data:row-major`, `event:timer-interrupt`, `lang:assembly`, `lang:c`, `peripheral:led`, `peripheral:timer`, `risk:bounds`, `risk:irq-shared-state`, `risk:lost-events`, `risk:stack-balance`, `risk:timer-ownership`, `risk:unreachable-destination`, `timing:periodic-500-ms`, `type:assembly-algorithm`, `type:c-board-state-machine`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FLOOD-FILL-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Questions

### Q1 - ASM

Compute a shortest path through a two-dimensional byte maze while respecting walls, bounds and distance updates.

- Type: `assembly-algorithm`
- Algorithms: `unweighted-shortest-path;maze-propagation`
- Peripherals/events/timing: `none`
- Data/ABI: `byte-matrix;callee-saved-registers;row-major`
- Risks: `bounds;unreachable-destination;stack-balance`
- Search words: shortest path maze distance walls wavefront
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-FLOOD-FILL-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`

### Q2 - C

Configure a timer for a 0.5-second sequence and move an LED indication through the required states without losing events.

- Type: `c-board-state-machine`
- Algorithms: `led-sequence`
- Peripherals/events/timing: `led;periodic-500-ms;timer;timer-interrupt`
- Data/ABI: `callback`
- Risks: `irq-shared-state;timer-ownership;lost-events`
- Search words: 0.5 second periodic LED sequence states
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

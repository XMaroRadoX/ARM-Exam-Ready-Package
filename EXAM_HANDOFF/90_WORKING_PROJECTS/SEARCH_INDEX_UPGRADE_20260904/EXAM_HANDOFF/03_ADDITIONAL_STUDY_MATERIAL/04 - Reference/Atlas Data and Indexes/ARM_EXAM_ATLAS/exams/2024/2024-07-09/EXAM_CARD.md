# E2024-07-09

- Date: `2024-07-09`
- Variant: `ARM`
- Source PDF: `Exams/23-24/20240709 arm.pdf`
- SHA-256: `072489aedf62543620d5bb60295fb085204bae358d5316fb342c1150475a9a98`
- Answer collection: `Study Material/03 - Solved Exams/2024-07-09_DFS_SysTick`
- Search tags: `abi:callee-saved-registers`, `abi:four-register-arguments`, `abi:non-leaf`, `abi:reset-handler`, `algorithm:available-moves`, `algorithm:depth-first-search`, `algorithm:explicit-stack`, `algorithm:maze`, `algorithm:modulo-selection`, `data:byte-matrix`, `data:candidate-array`, `data:explicit-stack`, `data:row-major`, `event:systick-interrupt`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `peripheral:systick`, `risk:bounds`, `risk:direct-register-setup`, `risk:stack-balance`, `risk:stack-capacity`, `risk:vector-ownership`, `timing:periodic`, `type:assembly-algorithm`, `type:assembly-startup-exception`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-DFS-STACK-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-DS-STACK-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Questions

### Q1 - ASM

Solve a maze with depth-first search using an explicit stack, four parameters and a nested call to chooseNeighbor.

- Type: `assembly-algorithm`
- Algorithms: `depth-first-search;explicit-stack;maze`
- Peripherals/events/timing: `none`
- Data/ABI: `byte-matrix;callee-saved-registers;explicit-stack;four-register-arguments;non-leaf;row-major`
- Risks: `stack-capacity;bounds;stack-balance`
- Search words: DFS chooseNeighbor explicit stack maze four parameters
- Pattern IDs: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-DFS-STACK-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-DS-STACK-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`

### Q2 - ASM startup/exception

Configure SysTick directly in Reset_Handler, collect available moves, choose one using modulo arithmetic, and keep the stack balanced across all branches.

- Type: `assembly-startup-exception`
- Algorithms: `available-moves;modulo-selection`
- Peripherals/events/timing: `periodic;systick;systick-interrupt`
- Data/ABI: `byte-matrix;candidate-array;non-leaf;reset-handler`
- Risks: `direct-register-setup;stack-balance;vector-ownership`
- Search words: Reset_Handler SysTick available moves modulo choose neighbor
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-MEM-BYTE-ARRAY-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

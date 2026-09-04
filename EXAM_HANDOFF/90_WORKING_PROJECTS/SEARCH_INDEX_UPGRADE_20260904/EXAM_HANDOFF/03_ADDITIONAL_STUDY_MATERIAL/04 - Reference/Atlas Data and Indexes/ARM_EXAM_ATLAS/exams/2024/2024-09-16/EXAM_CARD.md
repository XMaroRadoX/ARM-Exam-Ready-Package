# E2024-09-16

- Date: `2024-09-16`
- Variant: `ARM`
- Source PDF: `Exams/23-24/20240916 arm.pdf`
- SHA-256: `bbadd5254928052d8fdf6f824af902ed80a57c58adbb8028e7ec666d2935e3c1`
- Answer collection: `Study Material/03 - Solved Exams/2024-09-16_Kruskal_Buttons`
- Search tags: `abi:callback`, `abi:callee-saved-registers`, `abi:non-leaf`, `abi:seven-arguments`, `abi:stacked-arguments`, `algorithm:button-ordered-offset`, `algorithm:component-label-merge`, `algorithm:kruskal`, `algorithm:min-max-reduction`, `data:row-major`, `data:three-word-arrays`, `event:int0`, `event:key1`, `event:key2`, `lang:assembly`, `lang:c`, `peripheral:buttons`, `peripheral:led`, `risk:bounds`, `risk:debounce`, `risk:event-order`, `risk:irq-shared-state`, `risk:stack-balance`, `risk:stacked-offsets`, `type:assembly-algorithm`, `type:c-board-state-machine`
- Patterns: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-COMPONENT-MERGE-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-REDUCTION-001`, `PAT-DS-UNION-FIND-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Questions

### Q1 - ASM

Implement the Kruskal-style maze operation across three arrays with seven parameters, including min/max selection, component replacement and row-major access.

- Type: `assembly-algorithm`
- Algorithms: `kruskal;component-label-merge;min-max-reduction`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;non-leaf;row-major;seven-arguments;stacked-arguments;three-word-arrays`
- Risks: `stacked-offsets;bounds;stack-balance`
- Search words: Kruskal MST component replacement seven parameters min max
- Pattern IDs: `PAT-AAPCS-FOUR-ARGS-001`, `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-COMPONENT-MERGE-001`, `PAT-ALG-GRAPH-SEARCH-001`, `PAT-ALG-REDUCTION-001`, `PAT-DS-UNION-FIND-001`, `PAT-FLOW-NESTED-LOOP-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`

### Q2 - C

Implement a two-button state machine that increments a value and applies the required offset while handling event order and button behavior.

- Type: `c-board-state-machine`
- Algorithms: `button-ordered-offset`
- Peripherals/events/timing: `buttons;int0;key1;key2;led`
- Data/ABI: `callback`
- Risks: `debounce;event-order;irq-shared-state`
- Search words: two button state machine increment offset event order
- Pattern IDs: `PAT-GPIO-EVENT-001`, `PAT-STATE-DEBOUNCE-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.

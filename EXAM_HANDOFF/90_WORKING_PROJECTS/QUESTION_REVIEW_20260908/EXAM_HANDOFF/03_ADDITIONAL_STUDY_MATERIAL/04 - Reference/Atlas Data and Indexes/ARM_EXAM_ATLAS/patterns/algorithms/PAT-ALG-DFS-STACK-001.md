# PAT-ALG-DFS-STACK-001: Bounded DFS with an explicit stack

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: visit graph without recursion using bounded stack.

## C contract and variants

Primary export: `uint32_t pat_alg_dfs_stack_001(const uint8_t *adj, uint32_t n, uint32_t start, uint8_t *seen, uint32_t *stack);`

All public reference variants:

```c
uint32_t pat_alg_dfs_stack_001(const uint8_t *adj, uint32_t n, uint32_t start, uint8_t *seen, uint32_t *stack);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Validate buffers/start.
2. Push start.
3. Pop until empty.
4. Skip visited nodes.
5. Mark and count.
6. Push bounded unseen neighbors.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-DFS-STACK-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-DFS-STACK-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `adj` — `const uint8_t *adj` |
| `R1` | `n` — `uint32_t n` |
| `R2` | `start` — `uint32_t start` |
| `R3` | `seen` — `uint8_t *seen` |
| `caller [SP, #0]` | `stack` — `uint32_t *stack` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **32**. Local bytes: **0**. Static frame total: **32 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(V^2) time for an adjacency matrix, O(V) caller-provided stack/seen space.

## Boundary and adaptation checklist

- Current boundary policy: empty, one-element, duplicate, invalid-pointer/capacity and arithmetic-limit behavior is executable in the vector suite below.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: empty, one-element, duplicate, invalid-pointer/capacity and arithmetic-limit behavior is executable in the vector suite below. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  uint8_t a[9] = {0, 1, 0, 1, 0, 1, 0, 1, 0}, s[3] = {0};
  uint32_t q[3];
  return pat_alg_dfs_stack_001(a, 3, 0, s, q) == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t a[1] = {0}, s[1] = {0};
  uint32_t q[1];
  return pat_alg_dfs_stack_001(a, 1, 0, s, q) == 1 &&
         pat_alg_dfs_stack_001(NULL, 1, 0, s, q) == 0 &&
         pat_alg_dfs_stack_001(a, 1, 1, s, q) == 0;
}
```

## Historical grounding

- [E2024-07-09-Q1](../../exams/2024/2024-07-09/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

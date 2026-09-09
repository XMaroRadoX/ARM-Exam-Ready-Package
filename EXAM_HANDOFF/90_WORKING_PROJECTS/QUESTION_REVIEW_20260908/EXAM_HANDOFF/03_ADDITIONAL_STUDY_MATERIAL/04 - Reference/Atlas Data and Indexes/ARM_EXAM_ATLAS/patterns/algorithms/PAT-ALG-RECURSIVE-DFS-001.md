# PAT-ALG-RECURSIVE-DFS-001: Recursive DFS with depth contract

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: recursive graph traversal bounded depth.

## C contract and variants

Primary export: `uint32_t pat_alg_recursive_dfs_001(const uint8_t *a, uint32_t n, uint32_t start, uint8_t *s);`

All public reference variants:

```c
uint32_t pat_alg_recursive_dfs_001(const uint8_t *a, uint32_t n, uint32_t start, uint8_t *s);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Reject invalid start.
2. Mark current vertex.
3. Recursively visit unseen adjacent vertices while depth is bounded by n.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-RECURSIVE-DFS-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-RECURSIVE-DFS-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `a` — `const uint8_t *a` |
| `R1` | `n` — `uint32_t n` |
| `R2` | `start` — `uint32_t start` |
| `R3` | `s` — `uint8_t *s` |

`R0` carries `uint32_t`.

Classification: **non-leaf**. Saved-register bytes: **8**. Local bytes: **8**. Static frame total: **16 bytes**.

Calls: `visit`. SP must be eight-byte aligned at each public call boundary. Recursive code uses this frame per active call.

## Complexity

O(V^2) with adjacency matrix, O(V) maximum recursion/seen space.

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
  return pat_alg_recursive_dfs_001(a, 3, 0, s) == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t a[1] = {0}, s[1] = {0};
  return pat_alg_recursive_dfs_001(a, 1, 0, s) == 1 &&
         pat_alg_recursive_dfs_001(a, 1, 1, s) == 0 &&
         pat_alg_recursive_dfs_001(NULL, 1, 0, s) == 0;
}
```

## Historical grounding

No historical occurrence is claimed; this entry is supplementary preparation.

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `COMPILE_ONLY`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

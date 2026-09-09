# PAT-ALG-PREFIX-SUM-001: Prefix sums and range sums

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: precompute cumulative sums answer ranges.

## C contract and variants

Primary export: `int pat_alg_prefix_sum_001(const int32_t *values, uint32_t count, int64_t *prefix);`

All public reference variants:

```c
int pat_alg_prefix_sum_001(const int32_t *values, uint32_t count, int64_t *prefix);
int pat_alg_prefix_sum_001_range(const int64_t *prefix, uint32_t count, uint32_t begin, uint32_t end, int64_t *sum);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Write prefix[0]=0.
2. Accumulate each element into prefix[i+1].
3. Answer [begin,end) as prefix[end]-prefix[begin].

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-PREFIX-SUM-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-PREFIX-SUM-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `values` — `const int32_t *values` |
| `R1` | `count` — `uint32_t count` |
| `R2:R3` | `prefix` — `int64_t *prefix` |

`R0` carries `int`.

Classification: **leaf**. Saved-register bytes: **8**. Local bytes: **0**. Static frame total: **8 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(n) preprocessing, O(1) per range, O(n) prefix output.

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
  int32_t a[] = {1, -2, 4};
  int64_t p[4];
  pat_alg_prefix_sum_001(a, 3, p);
  return p[0] == 0 && p[1] == 1 && p[2] == -1 && p[3] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, -2, 4};
  int64_t p[4], s = 0;
  return pat_alg_prefix_sum_001(NULL, 0, p) &&
         pat_alg_prefix_sum_001(a, 3, p) &&
         pat_alg_prefix_sum_001_range(p, 3, 1, 3, &s) && s == 2 &&
         !pat_alg_prefix_sum_001_range(p, 3, 3, 2, &s);
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

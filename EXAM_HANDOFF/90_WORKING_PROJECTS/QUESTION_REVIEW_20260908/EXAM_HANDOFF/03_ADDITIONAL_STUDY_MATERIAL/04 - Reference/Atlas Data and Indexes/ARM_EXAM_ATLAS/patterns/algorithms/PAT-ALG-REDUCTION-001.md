# PAT-ALG-REDUCTION-001: Signed min max and sum reduction

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: reduce array to minimum maximum and sum.

## C contract and variants

Primary export: `int pat_alg_reduction_001(const int32_t *values, uint32_t count, pat_alg_reduction_001_signed_result_t *result);`

All public reference variants:

```c
int pat_alg_reduction_001(const int32_t *values, uint32_t count, pat_alg_reduction_001_signed_result_t *result);
int pat_alg_reduction_001_unsigned(const uint32_t *values, uint32_t count, pat_alg_reduction_001_unsigned_result_t *result);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Initialize min/max from first element and sum from zero.
2. Scan once.
3. Update signed comparisons.
4. Accumulate widened sum.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-REDUCTION-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-REDUCTION-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `values` — `const int32_t *values` |
| `R1` | `count` — `uint32_t count` |
| `R2` | `result` — `pat_alg_reduction_001_signed_result_t *result` |

`R0` carries `int`.

Classification: **leaf**. Saved-register bytes: **32**. Local bytes: **0**. Static frame total: **32 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(n) time, O(1) space.

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
  int32_t a[] = {-2, 5, 1};
  pat_alg_reduction_001_signed_result_t r;
  return pat_alg_reduction_001(a, 3, &r) && r.minimum == -2 && r.maximum == 5 &&
         r.sum == 4;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {INT32_MIN, INT32_MAX};
  uint32_t u[] = {0, UINT32_MAX};
  pat_alg_reduction_001_signed_result_t s;
  pat_alg_reduction_001_unsigned_result_t r;
  return !pat_alg_reduction_001(NULL, 0, &s) &&
         pat_alg_reduction_001(a, 2, &s) && s.sum == -1 &&
         pat_alg_reduction_001_unsigned(u, 2, &r) && r.sum == UINT32_MAX;
}
```

## Historical grounding

- [E2026-02-18-A1-Q1](../../exams/2026/2026-02-18-A1/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

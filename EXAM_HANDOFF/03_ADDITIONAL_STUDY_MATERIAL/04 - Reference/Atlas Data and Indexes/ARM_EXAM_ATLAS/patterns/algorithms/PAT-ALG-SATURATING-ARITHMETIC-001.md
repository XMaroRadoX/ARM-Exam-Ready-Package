# PAT-ALG-SATURATING-ARITHMETIC-001: Clamp absolute saturation and overflow

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: clamp signed arithmetic without overflow.

## C contract and variants

Primary export: `int32_t pat_alg_saturating_arithmetic_001(int64_t value, int32_t minimum, int32_t maximum);`

All public reference variants:

```c
int32_t pat_alg_saturating_arithmetic_001(int64_t value, int32_t minimum, int32_t maximum);
uint32_t pat_alg_saturating_arithmetic_001_abs_i32(int32_t value);
int32_t pat_alg_saturating_arithmetic_001_add_i32(int32_t first, int32_t second);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Compare widened value to bounds.
2. Clamp outside values.
3. Compute absolute through int64.
4. Use widened addition before saturation.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-SATURATING-ARITHMETIC-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-SATURATING-ARITHMETIC-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0:R1` | `value` — `int64_t value` |
| `R2` | `minimum` — `int32_t minimum` |
| `R3` | `maximum` — `int32_t maximum` |

`R0` carries `int32_t`.

Classification: **leaf**. Saved-register bytes: **8**. Local bytes: **0**. Static frame total: **8 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(1) time and space.

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
  return pat_alg_saturating_arithmetic_001(50, 0, 10) == 10 &&
         pat_alg_saturating_arithmetic_001(-2, 0, 10) == 0;
}
static int pattern_edge_vectors(void) {
  return pat_alg_saturating_arithmetic_001(5, 10, 0) == 10 &&
         pat_alg_saturating_arithmetic_001_abs_i32(INT32_MIN) ==
             UINT32_C(2147483648) &&
         pat_alg_saturating_arithmetic_001_add_i32(INT32_MAX, 1) == INT32_MAX &&
         pat_alg_saturating_arithmetic_001_add_i32(INT32_MIN, -1) == INT32_MIN;
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

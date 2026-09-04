# PAT-ALG-MOVING-AVERAGE-001: Moving average and sliding window

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: fixed window running sum average.

## C contract and variants

Primary export: `uint32_t pat_alg_moving_average_001(const int32_t *a, uint32_t n, uint32_t w, int32_t *out);`

All public reference variants:

```c
uint32_t pat_alg_moving_average_001(const int32_t *a, uint32_t n, uint32_t w, int32_t *out);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Add entering item to running sum.
2. Subtract leaving item once window is full.
3. Emit sum/window.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-MOVING-AVERAGE-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-MOVING-AVERAGE-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

Runtime imports: `__aeabi_ldivmod`. Link the compiler runtime when copying this implementation.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `a` — `const int32_t *a` |
| `R1` | `n` — `uint32_t n` |
| `R2` | `w` — `uint32_t w` |
| `R3` | `out` — `int32_t *out` |

`R0` carries `uint32_t`.

Classification: **non-leaf**. Saved-register bytes: **36**. Local bytes: **12**. Static frame total: **48 bytes**.

Calls: `__aeabi_ldivmod`. SP must be eight-byte aligned at each public call boundary. Recursive code uses this frame per active call.

## Complexity

O(n) time, O(1) internal space plus output.

## Boundary and adaptation checklist

- Current boundary policy: zero or oversized windows return no output; division uses C signed truncation toward zero.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: zero or oversized windows return no output; division uses C signed truncation toward zero. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {1, 2, 3}, o[2];
  return pat_alg_moving_average_001(a, 3, 2, o) == 2 && o[0] == 1 && o[1] == 2;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, 2, 3}, o[3];
  return pat_alg_moving_average_001(a, 3, 0, o) == 0 &&
         pat_alg_moving_average_001(a, 3, 4, o) == 0 &&
         pat_alg_moving_average_001(a, 3, 1, o) == 3 && o[2] == 3;
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

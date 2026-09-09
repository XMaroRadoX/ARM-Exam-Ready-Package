# PAT-ALG-HISTOGRAM-MODE-001: Histogram frequency and mode

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: count bounded values choose mode.

## C contract and variants

Primary export: `uint32_t pat_alg_histogram_mode_001(const uint8_t *a, uint32_t n, uint32_t range, uint32_t *freq);`

All public reference variants:

```c
uint32_t pat_alg_histogram_mode_001(const uint8_t *a, uint32_t n, uint32_t range, uint32_t *freq);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Zero bounded frequencies.
2. Count only in-range keys.
3. Scan frequencies and retain first greatest mode.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-HISTOGRAM-MODE-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-HISTOGRAM-MODE-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

Runtime imports: `__aeabi_memclr4`. Link the compiler runtime when copying this implementation.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `a` — `const uint8_t *a` |
| `R1` | `n` — `uint32_t n` |
| `R2` | `range` — `uint32_t range` |
| `R3` | `freq` — `uint32_t *freq` |

`R0` carries `uint32_t`.

Classification: **non-leaf**. Saved-register bytes: **20**. Local bytes: **0**. Static frame total: **20 bytes**.

Calls: `__aeabi_memclr4`. SP must be eight-byte aligned at each public call boundary. Recursive code uses this frame per active call.

## Complexity

O(n+k) time, O(k) caller frequency space.

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
  uint8_t a[] = {2, 1, 2};
  uint32_t f[3];
  return pat_alg_histogram_mode_001(a, 3, 3, f) == 2 && f[2] == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {2, 2, 1, 9};
  uint32_t f[3];
  return pat_alg_histogram_mode_001(a, 4, 3, f) == 2 && f[2] == 2;
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

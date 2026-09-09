# PAT-ALG-COUNTING-SORT-001: Bounded counting sort

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: sort keys in known small range.

## C contract and variants

Primary export: `int pat_alg_counting_sort_001(uint8_t *a, uint32_t n, uint32_t range, uint32_t *count);`

All public reference variants:

```c
int pat_alg_counting_sort_001(uint8_t *a, uint32_t n, uint32_t range, uint32_t *count);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Zero frequency table.
2. Validate and count keys.
3. Emit each key frequency times.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-COUNTING-SORT-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-COUNTING-SORT-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

Runtime imports: `__aeabi_memclr4`. Link the compiler runtime when copying this implementation.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `a` — `uint8_t *a` |
| `R1` | `n` — `uint32_t n` |
| `R2` | `range` — `uint32_t range` |
| `R3` | `count` — `uint32_t *count` |

`R0` carries `int`.

Classification: **non-leaf**. Saved-register bytes: **20**. Local bytes: **0**. Static frame total: **20 bytes**.

Calls: `__aeabi_memclr4`. SP must be eight-byte aligned at each public call boundary. Recursive code uses this frame per active call.

## Complexity

O(n+k) time, O(k) caller frequency space.

## Boundary and adaptation checklist

- Current boundary policy: keys outside range fail; range above 256 fails; count table must have range entries.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: keys outside range fail; range above 256 fails; count table must have range entries. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  uint8_t a[] = {3, 1, 2, 1};
  uint32_t c[4];
  return pat_alg_counting_sort_001(a, 4, 4, c) && a[0] == 1 && a[1] == 1 &&
         a[2] == 2 && a[3] == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {0, 3};
  uint32_t c[4];
  return pat_alg_counting_sort_001(a, 0, 4, c) &&
         !pat_alg_counting_sort_001(a, 2, 3, c) &&
         !pat_alg_counting_sort_001(NULL, 1, 4, c);
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

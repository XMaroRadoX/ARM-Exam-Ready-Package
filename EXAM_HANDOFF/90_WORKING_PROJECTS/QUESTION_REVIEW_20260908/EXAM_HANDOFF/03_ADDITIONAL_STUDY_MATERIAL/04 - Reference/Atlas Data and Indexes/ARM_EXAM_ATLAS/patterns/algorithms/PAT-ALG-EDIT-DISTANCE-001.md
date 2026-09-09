# PAT-ALG-EDIT-DISTANCE-001: Edit distance

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: insert delete substitute dynamic programming.

## C contract and variants

Primary export: `uint32_t pat_alg_edit_distance_001(const char *first, const char *second, uint32_t first_length, uint32_t second_length, uint32_t *previous, uint32_t *current);`

All public reference variants:

```c
uint32_t pat_alg_edit_distance_001(const char *first, const char *second, uint32_t first_length, uint32_t second_length, uint32_t *previous, uint32_t *current);
uint32_t pat_alg_edit_distance_001_full(const char *first, const char *second, uint32_t first_length, uint32_t second_length, uint32_t *table, uint32_t table_elements);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Initialize first row/column.
2. For each character pair compute delete/insert/substitute.
3. Keep minimum.
4. Use either full table or two rows.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-EDIT-DISTANCE-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-EDIT-DISTANCE-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `first` — `const char *first` |
| `R1` | `second` — `const char *second` |
| `R2` | `first_length` — `uint32_t first_length` |
| `R3` | `second_length` — `uint32_t second_length` |
| `caller [SP, #0]` | `previous` — `uint32_t *previous` |
| `caller [SP, #4]` | `current` — `uint32_t *current` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **36**. Local bytes: **24**. Static frame total: **60 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(a*b) time; O(a*b) full-table or O(b) two-row space.

## Boundary and adaptation checklist

- Current boundary policy: null buffers return UINT32_MAX; caller supplies second_length+1 row buffers or the full table size.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: null buffers return UINT32_MAX; caller supplies second_length+1 row buffers or the full table size. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  uint32_t p[8], c[8];
  return pat_alg_edit_distance_001("kitten", "sitting", 6, 7, p, c) == 3;
}
static int pattern_edge_vectors(void) {
  uint32_t p[4], c[4], t[16];
  return pat_alg_edit_distance_001("", "abc", 0, 3, p, c) == 3 &&
         pat_alg_edit_distance_001("abc", "", 3, 0, p, c) == 3 &&
         pat_alg_edit_distance_001_full("abc", "adc", 3, 3, t, 16) == 1 &&
         pat_alg_edit_distance_001_full("a", "b", 1, 1, t, 3) == UINT32_MAX;
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

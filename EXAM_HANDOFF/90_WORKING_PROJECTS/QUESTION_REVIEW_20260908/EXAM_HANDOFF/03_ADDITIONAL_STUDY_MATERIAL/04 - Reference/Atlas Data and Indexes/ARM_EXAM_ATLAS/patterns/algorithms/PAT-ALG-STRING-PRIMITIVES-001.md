# PAT-ALG-STRING-PRIMITIVES-001: Bounded string primitives

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: length comparison search bounded copy.

## C contract and variants

Primary export: `int32_t pat_alg_string_primitives_001(const char *text, const char *needle, uint32_t limit);`

All public reference variants:

```c
uint32_t pat_alg_string_primitives_001_length(const char *text, uint32_t limit);
int32_t pat_alg_string_primitives_001_compare(const char *first, const char *second, uint32_t limit);
uint32_t pat_alg_string_primitives_001_copy(char *destination, uint32_t capacity, const char *source);
int32_t pat_alg_string_primitives_001(const char *text, const char *needle, uint32_t limit);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Scan with explicit limit for length.
2. Compare unsigned bytes.
3. Bounded-copy with terminator.
4. Test each possible substring start.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-STRING-PRIMITIVES-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-STRING-PRIMITIVES-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `text` — `const char *text` |
| `R1` | `needle` — `const char *needle` |
| `R2` | `limit` — `uint32_t limit` |

`R0` carries `int32_t`.

Classification: **leaf**. Saved-register bytes: **32**. Local bytes: **0**. Static frame total: **32 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(limit) for length/compare/copy and O(limit*needle length) for naive search.

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
  return pat_alg_string_primitives_001("abcabc", "cab", 6) == 2 &&
         pat_alg_string_primitives_001("abc", "z", 3) == -1;
}
static int pattern_edge_vectors(void) {
  char out[4];
  return pat_alg_string_primitives_001_length("abc", 2) == 2 &&
         pat_alg_string_primitives_001_compare("a", "b", 2) < 0 &&
         pat_alg_string_primitives_001_copy(out, 4, "abcd") == 3 &&
         out[3] == '\0' && pat_alg_string_primitives_001("", "", 1) == 0 &&
         pat_alg_string_primitives_001(NULL, "a", 1) == -1;
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

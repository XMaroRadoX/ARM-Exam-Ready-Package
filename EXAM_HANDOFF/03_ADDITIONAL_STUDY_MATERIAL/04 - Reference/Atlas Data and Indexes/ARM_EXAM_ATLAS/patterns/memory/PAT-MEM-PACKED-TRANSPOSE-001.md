# PAT-MEM-PACKED-TRANSPOSE-001: Packed 8x8 bit-matrix transpose

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: transpose packed binary matrix rows and columns.

## C contract and variants

Primary export: `uint64_t pat_mem_packed_transpose_001(uint64_t x);`

All public reference variants:

```c
uint64_t pat_mem_packed_transpose_001(uint64_t x);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Clear output.
2. For every source row and column.
3. Extract one bit.
4. Insert it at column,row.
5. Return packed output.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-MEM-PACKED-TRANSPOSE-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-MEM-PACKED-TRANSPOSE-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0:R1` | `x` — `uint64_t x` |

`R0:R1` carries `uint64_t` low word then high word.

Classification: **leaf**. Saved-register bytes: **24**. Local bytes: **0**. Static frame total: **24 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(64) time, O(1) space.

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
  return pat_mem_packed_transpose_001(UINT64_C(1) << 10) == (UINT64_C(1) << 17);
}
static int pattern_edge_vectors(void) {
  uint64_t x = UINT64_C(0x0123456789abcdef);
  return pat_mem_packed_transpose_001(0) == 0 &&
         pat_mem_packed_transpose_001(pat_mem_packed_transpose_001(x)) == x;
}
```

## Historical grounding

- [E2025-01-29-A3-Q1](../../exams/2025/2025-01-29-A3/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

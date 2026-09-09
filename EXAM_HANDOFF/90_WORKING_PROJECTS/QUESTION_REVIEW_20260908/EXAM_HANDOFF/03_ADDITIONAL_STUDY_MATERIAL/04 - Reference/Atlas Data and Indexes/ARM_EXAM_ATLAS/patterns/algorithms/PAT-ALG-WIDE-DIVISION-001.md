# PAT-ALG-WIDE-DIVISION-001: Signed 64-by-32 restoring division

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: divide signed 64-bit dividend by signed 32-bit divisor.

## C contract and variants

Primary export: `int64_t pat_alg_wide_division_001(int64_t dividend, int32_t divisor, int32_t *remainder);`

All public reference variants:

```c
int64_t pat_alg_wide_division_001(int64_t dividend, int32_t divisor, int32_t *remainder);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Reject zero divisor.
2. Normalize signs.
3. Repeat 64 shift/compare/subtract steps.
4. Restore quotient and remainder signs.
5. Return R0:R1.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-WIDE-DIVISION-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-WIDE-DIVISION-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0:R1` | `dividend` — `int64_t dividend` |
| `R2` | `divisor` — `int32_t divisor` |
| `R3` | `remainder` — `int32_t *remainder` |

`R0:R1` carries `int64_t` low word then high word.

Classification: **leaf**. Saved-register bytes: **32**. Local bytes: **8**. Static frame total: **40 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(64) time for fixed widths, O(1) space.

## Boundary and adaptation checklist

- Current boundary policy: divisor zero returns quotient/remainder zero; INT64_MIN is normalized without signed overflow.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: divisor zero returns quotient/remainder zero; INT64_MIN is normalized without signed overflow. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  int32_t r = 0;
  return pat_alg_wide_division_001(-15, 2, &r) == -7 && r == -1;
}
static int pattern_edge_vectors(void) {
  int32_t r = 7;
  return pat_alg_wide_division_001(0, 5, &r) == 0 && r == 0 &&
         pat_alg_wide_division_001(15, -2, &r) == -7 && r == 1 &&
         pat_alg_wide_division_001(9, 0, &r) == 0 && r == 0;
}
```

## Historical grounding

- [E2023-05-17-Q1](../../exams/2023/2023-05-17/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

# PAT-ALG-DECIMAL-DIGITS-001: Decimal digit algorithms

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: extract reconstruct sum palindrome Kaprekar digits.

## C contract and variants

Primary export: `uint32_t pat_alg_decimal_digits_001(uint32_t value);`

All public reference variants:

```c
uint32_t pat_alg_decimal_digits_001(uint32_t value);
uint32_t pat_alg_decimal_digits_001_extract(uint32_t value, uint8_t *digits, uint32_t capacity);
uint32_t pat_alg_decimal_digits_001_reconstruct(const uint8_t *digits, uint32_t count);
int pat_alg_decimal_digits_001_is_palindrome(uint32_t value);
uint32_t pat_alg_decimal_digits_001_kaprekar_4(uint32_t value);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Extract base-10 digits with remainder/division.
2. Reconstruct in reverse order.
3. Compare for palindrome.
4. Sort four digits for Kaprekar step.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-DECIMAL-DIGITS-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-DECIMAL-DIGITS-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `value` — `uint32_t value` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **16**. Local bytes: **0**. Static frame total: **16 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(number of digits), except fixed four-digit Kaprekar sorting.

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
  return pat_alg_decimal_digits_001(123) == ((6u << 16) | 321u);
}
static int pattern_edge_vectors(void) {
  uint8_t d[10];
  uint32_t n = pat_alg_decimal_digits_001_extract(1203, d, 10);
  return n == 4 && pat_alg_decimal_digits_001_reconstruct(d, n) == 1203 &&
         pat_alg_decimal_digits_001_is_palindrome(1221) &&
         !pat_alg_decimal_digits_001_is_palindrome(123) &&
         pat_alg_decimal_digits_001_kaprekar_4(3524) == 3087;
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

# PAT-ALG-PRIME-FACTORIZATION-001: Prime testing and trial factorization

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: test prime using divisors through square root.

## C contract and variants

Primary export: `int pat_alg_prime_factorization_001(uint32_t value);`

All public reference variants:

```c
int pat_alg_prime_factorization_001(uint32_t value);
uint32_t pat_alg_prime_factorization_001_factorize(uint32_t value, uint32_t *factors, uint32_t capacity);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Reject values below two.
2. Handle two/even values.
3. Try odd divisors through n/divisor.
4. Repeatedly divide to factorize.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-PRIME-FACTORIZATION-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-PRIME-FACTORIZATION-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `value` — `uint32_t value` |

`R0` carries `int`.

Classification: **leaf**. Saved-register bytes: **0**. Local bytes: **0**. Static frame total: **0 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(sqrt n) trial time; O(number of factors) output.

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
  return pat_alg_prime_factorization_001(29) &&
         !pat_alg_prime_factorization_001(21) &&
         !pat_alg_prime_factorization_001(1);
}
static int pattern_edge_vectors(void) {
  uint32_t f[4] = {0};
  return pat_alg_prime_factorization_001(2) &&
         !pat_alg_prime_factorization_001(0) &&
         pat_alg_prime_factorization_001_factorize(12, f, 4) == 3 &&
         f[0] == 2 && f[1] == 2 && f[2] == 3 &&
         pat_alg_prime_factorization_001_factorize(1, f, 4) == 0;
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

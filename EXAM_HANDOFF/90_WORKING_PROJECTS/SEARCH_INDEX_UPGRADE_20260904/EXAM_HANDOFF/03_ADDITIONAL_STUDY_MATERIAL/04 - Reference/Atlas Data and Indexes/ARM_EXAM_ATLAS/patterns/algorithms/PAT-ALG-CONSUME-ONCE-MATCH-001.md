# PAT-ALG-CONSUME-ONCE-MATCH-001: Consume-once duplicate-safe matching

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: Bulls and Cows Mastermind duplicate-safe match.

## C contract and variants

Primary export: `uint32_t pat_alg_consume_once_match_001(const uint8_t *secret, const uint8_t *guess, uint32_t n, uint32_t *cows);`

All public reference variants:

```c
uint32_t pat_alg_consume_once_match_001(const uint8_t *secret, const uint8_t *guess, uint32_t n, uint32_t *cows);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Mark exact matches in two used arrays.
2. For each unused guess scan unused secrets.
3. Consume the first equal value.
4. Return bulls and cows.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-CONSUME-ONCE-MATCH-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-CONSUME-ONCE-MATCH-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `secret` — `const uint8_t *secret` |
| `R1` | `guess` — `const uint8_t *guess` |
| `R2` | `n` — `uint32_t n` |
| `R3` | `cows` — `uint32_t *cows` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **32**. Local bytes: **64**. Static frame total: **96 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(n^2) time, O(n) bounded used-marker space.

## Boundary and adaptation checklist

- Current boundary policy: count zero produces zero; count above 32 is rejected; duplicate values are consumed only once.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: count zero produces zero; count above 32 is rejected; duplicate values are consumed only once. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  uint8_t s[] = {1, 1, 2, 3}, g[] = {1, 2, 1, 4};
  uint32_t c = 0;
  return pat_alg_consume_once_match_001(s, g, 4, &c) == 1 && c == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {1}, b[] = {2};
  uint32_t c = 9;
  return pat_alg_consume_once_match_001(a, b, 0, &c) == 0 && c == 0 &&
         pat_alg_consume_once_match_001(a, b, 1, &c) == 0 && c == 0 &&
         pat_alg_consume_once_match_001(a, b, 33, &c) == 0;
}
```

## Historical grounding

- [E2026-06-25-B1-Q1](../../exams/2026/2026-06-25-B1/Q1_ASSEMBLY.md)
- [E2026-06-25-B2-Q1](../../exams/2026/2026-06-25-B2/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

# PAT-ALG-LCG-001: Five-argument linear congruential generator

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: LCG modulo shifts and unsigned wraparound.

## C contract and variants

Primary export: `uint32_t pat_alg_lcg_001(uint32_t x, uint32_t a, uint32_t c, uint32_t m, uint32_t shift);`

All public reference variants:

```c
uint32_t pat_alg_lcg_001(uint32_t x, uint32_t a, uint32_t c, uint32_t m, uint32_t shift);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Compute a*x+c with 32-bit wraparound.
2. Apply modulus when nonzero.
3. Shift only when shift is below 32.
4. Return result.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-LCG-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-LCG-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `x` — `uint32_t x` |
| `R1` | `a` — `uint32_t a` |
| `R2` | `c` — `uint32_t c` |
| `R3` | `m` — `uint32_t m` |
| `caller [SP, #0]` | `shift` — `uint32_t shift` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **0**. Local bytes: **0**. Static frame total: **0 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(1) time and space.

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
  return pat_alg_lcg_001(1, 5, 3, 7, 0) == 1;
}
static int pattern_edge_vectors(void) {
  return pat_alg_lcg_001(1, 1, 1, 0, 0) == 2 &&
         pat_alg_lcg_001(1, 1, 1, 7, 32) == 0;
}
```

## Historical grounding

- [E2025-07-01-A1-Q1](../../exams/2025/2025-07-01-A1/Q1_ASSEMBLY.md)
- [E2025-07-01-A2-Q1](../../exams/2025/2025-07-01-A2/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

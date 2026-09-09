# PAT-ALG-COIN-CHANGE-001: Coin change

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: minimum coins or number of ways.

## C contract and variants

Primary export: `uint32_t pat_alg_coin_change_001(const uint16_t *coin, uint32_t n, uint32_t amount, uint32_t *dp);`

All public reference variants:

```c
uint32_t pat_alg_coin_change_001(const uint16_t *coin, uint32_t n, uint32_t amount, uint32_t *dp);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Initialize unreachable states and dp[0].
2. For each amount try every usable coin.
3. Keep minimum predecessor plus one.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-COIN-CHANGE-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-COIN-CHANGE-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

Runtime imports: `__aeabi_memset4`. Link the compiler runtime when copying this implementation.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `coin` — `const uint16_t *coin` |
| `R1` | `n` — `uint32_t n` |
| `R2` | `amount` — `uint32_t amount` |
| `R3` | `dp` — `uint32_t *dp` |

`R0` carries `uint32_t`.

Classification: **non-leaf**. Saved-register bytes: **32**. Local bytes: **0**. Static frame total: **32 bytes**.

Calls: `__aeabi_memset4`. SP must be eight-byte aligned at each public call boundary. Recursive code uses this frame per active call.

## Complexity

O(coins*amount) time, O(amount) space.

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
  uint16_t c[] = {1, 3};
  uint32_t d[5];
  return pat_alg_coin_change_001(c, 2, 4, d) == 2;
}
static int pattern_edge_vectors(void) {
  uint16_t c[] = {2};
  uint32_t d[4];
  return pat_alg_coin_change_001(c, 1, 0, d) == 0 &&
         pat_alg_coin_change_001(c, 1, 3, d) == UINT32_MAX;
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

# PAT-ALG-FAST-POWER-001: Exponentiation by squaring

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: fast power modular exponentiation.

## C contract and variants

Primary export: `uint32_t pat_alg_fast_power_001(uint32_t base, uint32_t exponent, uint32_t modulus);`

All public reference variants:

```c
uint32_t pat_alg_fast_power_001(uint32_t base, uint32_t exponent, uint32_t modulus);
int pat_alg_fast_power_001_checked(uint32_t base, uint32_t exponent, uint32_t *result);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Maintain accumulated result and squared factor.
2. Multiply on set exponent bits.
3. Square and shift exponent.
4. Optionally reduce modulo.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-FAST-POWER-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-FAST-POWER-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

Runtime imports: `__aeabi_uldivmod`. Link the compiler runtime when copying this implementation.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `base` — `uint32_t base` |
| `R1` | `exponent` — `uint32_t exponent` |
| `R2` | `modulus` — `uint32_t modulus` |

`R0` carries `uint32_t`.

Classification: **non-leaf**. Saved-register bytes: **32**. Local bytes: **0**. Static frame total: **32 bytes**.

Calls: `__aeabi_uldivmod, __aeabi_uldivmod`. SP must be eight-byte aligned at each public call boundary. Recursive code uses this frame per active call.

## Complexity

O(log exponent) time, O(1) space.

## Boundary and adaptation checklist

- Current boundary policy: zero exponent returns one (reduced when modulus is one); checked non-modular variant rejects overflow.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: zero exponent returns one (reduced when modulus is one); checked non-modular variant rejects overflow. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  return pat_alg_fast_power_001(3, 4, 5) == 1;
}
static int pattern_edge_vectors(void) {
  uint32_t out = 0;
  return pat_alg_fast_power_001(7, 0, 5) == 1 &&
         pat_alg_fast_power_001_checked(3, 4, &out) && out == 81 &&
         !pat_alg_fast_power_001_checked(UINT32_MAX, 2, &out);
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

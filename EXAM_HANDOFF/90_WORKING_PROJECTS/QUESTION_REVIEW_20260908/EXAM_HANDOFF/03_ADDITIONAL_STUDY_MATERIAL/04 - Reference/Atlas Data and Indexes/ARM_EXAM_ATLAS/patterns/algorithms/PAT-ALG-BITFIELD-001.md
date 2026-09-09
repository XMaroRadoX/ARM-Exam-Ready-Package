# PAT-ALG-BITFIELD-001: Bitfield extraction insertion and packing

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: mask shift pack unpack field.

## C contract and variants

Primary export: `uint32_t pat_alg_bitfield_001(uint32_t word, uint32_t value, uint32_t shift, uint32_t width);`

All public reference variants:

```c
uint32_t pat_alg_bitfield_001(uint32_t word, uint32_t value, uint32_t shift, uint32_t width);
uint32_t pat_alg_bitfield_001_extract(uint32_t word, uint32_t shift, uint32_t width);
uint32_t pat_alg_bitfield_001_pack_u16(uint16_t high, uint16_t low);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Validate shift/width.
2. Construct width mask.
3. Clear destination field.
4. Insert masked value.
5. Reverse with shift-and-mask extraction.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-BITFIELD-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-BITFIELD-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `word` — `uint32_t word` |
| `R1` | `value` — `uint32_t value` |
| `R2` | `shift` — `uint32_t shift` |
| `R3` | `width` — `uint32_t width` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **0**. Local bytes: **0**. Static frame total: **0 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(1) time and space.

## Boundary and adaptation checklist

- Current boundary policy: zero width or a field crossing bit 31 leaves insertion unchanged and extracts zero.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: zero width or a field crossing bit 31 leaves insertion unchanged and extracts zero. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  return pat_alg_bitfield_001(0, 3, 4, 2) == 0x30u;
}
static int pattern_edge_vectors(void) {
  return pat_alg_bitfield_001(UINT32_MAX, 0, 8, 8) == UINT32_C(0xffff00ff) &&
         pat_alg_bitfield_001_extract(UINT32_C(0x12345678), 8, 8) == 0x56 &&
         pat_alg_bitfield_001_pack_u16(0x1234, 0x5678) ==
             UINT32_C(0x12345678) &&
         pat_alg_bitfield_001(7, 0, 31, 2) == 7;
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

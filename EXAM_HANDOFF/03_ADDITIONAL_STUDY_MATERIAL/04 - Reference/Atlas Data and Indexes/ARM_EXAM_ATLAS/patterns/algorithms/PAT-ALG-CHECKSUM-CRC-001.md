# PAT-ALG-CHECKSUM-CRC-001: Checksums and CRC table structure

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: xor additive checksum table driven crc.

## C contract and variants

Primary export: `uint32_t pat_alg_checksum_crc_001(const uint8_t *bytes, uint32_t count);`

All public reference variants:

```c
uint32_t pat_alg_checksum_crc_001(const uint8_t *bytes, uint32_t count);
uint32_t pat_alg_checksum_crc_001_crc32_table(const uint8_t *bytes, uint32_t count, const uint32_t table[256]);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Scan bytes to update XOR and additive checksums.
2. For CRC use low-byte table index then shift/XOR state.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-CHECKSUM-CRC-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-CHECKSUM-CRC-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `bytes` — `const uint8_t *bytes` |
| `R1` | `count` — `uint32_t count` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **0**. Local bytes: **0**. Static frame total: **0 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(n) time, O(1) space plus a 256-word CRC table.

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
  uint8_t a[] = {1, 2};
  return pat_alg_checksum_crc_001(a, 2) == ((3u << 16) | 3u);
}
static int pattern_edge_vectors(void) {
  uint32_t table[256] = {0};
  uint8_t a[] = {1};
  return pat_alg_checksum_crc_001(NULL, 0) == 0 &&
         pat_alg_checksum_crc_001(a, 1) == ((1u << 16) | 1u) &&
         pat_alg_checksum_crc_001_crc32_table(a, 1, table) ==
             UINT32_C(0xff000000) &&
         pat_alg_checksum_crc_001_crc32_table(NULL, 1, table) == 0;
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

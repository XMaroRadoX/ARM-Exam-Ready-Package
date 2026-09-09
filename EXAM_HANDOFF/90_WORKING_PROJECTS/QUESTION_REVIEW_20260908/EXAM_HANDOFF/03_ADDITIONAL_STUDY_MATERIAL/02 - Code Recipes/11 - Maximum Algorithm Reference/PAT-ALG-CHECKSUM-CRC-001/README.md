# PAT-ALG-CHECKSUM-CRC-001: Checksums and CRC table structure

## Recognition phrases

Primary packs XOR checksum in bits 16..23 and additive checksum modulo 65536 in bits 0..15. CRC variant requires a caller-supplied reflected 256-word table.

## C contract and variants

```c
uint32_t pat_alg_checksum_crc_001(const uint8_t *bytes, uint32_t count);
uint32_t pat_alg_checksum_crc_001_crc32_table(const uint8_t *bytes, uint32_t count, const uint32_t table[256]);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Scan bytes to update XOR and additive checksums.
2. For CRC use low-byte table index then shift/XOR state.

## Worked trace

Bytes [1,2,3] have XOR 0 and sum 6; packed result 6.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_checksum_crc_001 | const uint8_t *bytes | R0 |
| pat_alg_checksum_crc_001 | uint32_t count | R1 |
| pat_alg_checksum_crc_001_crc32_table | const uint8_t *bytes | R0 |
| pat_alg_checksum_crc_001_crc32_table | uint32_t count | R1 |
| pat_alg_checksum_crc_001_crc32_table | const uint32_t table[256] | R2 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) time, O(1) space plus a 256-word CRC table.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

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
         pat_alg_checksum_crc_001_crc32_table(a, 1, table) == UINT32_C(0xff000000) &&
         pat_alg_checksum_crc_001_crc32_table(NULL, 1, table) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int main(void) { return pattern_test_suite(); }
```

## Historical grounding

This page is a reusable study method or possible variation. It does not claim
that its complete interface appeared verbatim in a paper. Use the package's
original papers and solved-exam pages for the exact required signatures.

## Verification boundary

Behavioral execution and portal structure are separate checks. LLVM validation
translates ARMASM directives to GNU assembler directives while retaining the
instruction stream. ARM execution uses an emulator; supported external 64-bit
division helpers are modeled at their ARM runtime ABI. Native Keil assembly and
physical-board execution are separate gates and are not implied by these tests.

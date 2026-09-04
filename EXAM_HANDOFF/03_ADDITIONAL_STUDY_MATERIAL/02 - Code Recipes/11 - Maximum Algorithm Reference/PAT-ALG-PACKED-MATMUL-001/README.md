# PAT-ALG-PACKED-MATMUL-001: Packed binary matrix multiplication

## Recognition phrases

Packed 8x8 binary matrices; bit 8*r+c represents cell(r,c). Multiplication is over GF(2): XOR the AND products.

## C contract and variants

```c
uint64_t pat_alg_packed_matmul_001(uint64_t a, uint64_t b);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Clear output.
2. For every result row and column.
3. XOR the eight pairwise AND products.
4. Set the packed result bit.

## Worked trace

Multiplying any packed matrix by the binary identity preserves it.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_packed_matmul_001 | uint64_t a | R0:R1 |
| pat_alg_packed_matmul_001 | uint64_t b | R2:R3 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(8^3) time, O(1) space for fixed 8x8 matrices.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint64_t i = UINT64_C(0x8040201008040201);
  return pat_alg_packed_matmul_001(i, i) == i;
}
static int pattern_edge_vectors(void) {
  uint64_t identity = UINT64_C(0x8040201008040201);
  return pat_alg_packed_matmul_001(0, identity) == 0 &&
         pat_alg_packed_matmul_001(identity, 0) == 0;
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

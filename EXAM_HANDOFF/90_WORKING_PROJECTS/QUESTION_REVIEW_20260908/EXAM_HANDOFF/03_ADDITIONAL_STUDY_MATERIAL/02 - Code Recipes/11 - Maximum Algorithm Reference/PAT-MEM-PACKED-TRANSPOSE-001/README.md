# PAT-MEM-PACKED-TRANSPOSE-001: Packed 8x8 bit-matrix transpose

## Recognition phrases

Packed 8x8 bit matrix: move bit 8*r+c to bit 8*c+r.

## C contract and variants

```c
uint64_t pat_mem_packed_transpose_001(uint64_t x);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Clear output.
2. For every source row and column.
3. Extract one bit.
4. Insert it at column,row.
5. Return packed output.

## Worked trace

A bit at (0,1), value 2, moves to (1,0), value 256.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_mem_packed_transpose_001 | uint64_t x | R0:R1 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(64) time, O(1) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  return pat_mem_packed_transpose_001(UINT64_C(1) << 10) == (UINT64_C(1) << 17);
}
static int pattern_edge_vectors(void) {
  uint64_t x = UINT64_C(0x0123456789abcdef);
  return pat_mem_packed_transpose_001(0) == 0 &&
         pat_mem_packed_transpose_001(pat_mem_packed_transpose_001(x)) == x;
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

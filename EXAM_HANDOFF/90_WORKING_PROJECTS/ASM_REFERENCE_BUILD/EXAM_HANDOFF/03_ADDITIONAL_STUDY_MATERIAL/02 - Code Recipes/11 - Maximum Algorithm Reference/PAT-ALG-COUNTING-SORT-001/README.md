# PAT-ALG-COUNTING-SORT-001: Bounded counting sort

## Recognition phrases

Unsigned bytes, range<=256, caller count array has range words. Reject an out-of-range value before output sorting. Scratch frequencies are consumed to zero.

## C contract and variants

```c
int pat_alg_counting_sort_001(uint8_t *a, uint32_t n, uint32_t range, uint32_t *count);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Zero frequency table.
2. Validate and count keys.
3. Emit each key frequency times.

## Worked trace

[2,0,2], range 3 -> [0,2,2]; counters finish [0,0,0].

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_counting_sort_001 | uint8_t *a | R0 |
| pat_alg_counting_sort_001 | uint32_t n | R1 |
| pat_alg_counting_sort_001 | uint32_t range | R2 |
| pat_alg_counting_sort_001 | uint32_t *count | R3 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n+k) time, O(k) caller frequency space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint8_t a[] = {3, 1, 2, 1};
  uint32_t c[4];
  return pat_alg_counting_sort_001(a, 4, 4, c) && a[0] == 1 && a[1] == 1 && a[2] == 2 &&
         a[3] == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t check_a[3] = {2, 0, 2};
  uint32_t check_c[3];
  if (!pat_alg_counting_sort_001(check_a, 3, 3, check_c) || check_c[0] || check_c[1] ||
      check_c[2])
    return 0;
  uint8_t a[] = {0, 3};
  uint32_t c[4];
  return pat_alg_counting_sort_001(a, 0, 4, c) &&
         !pat_alg_counting_sort_001(a, 2, 3, c) &&
         !pat_alg_counting_sort_001(NULL, 1, 4, c);
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

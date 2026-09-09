# PAT-ALG-LIS-001: Longest increasing subsequence

## Recognition phrases

Strictly increasing subsequence length, not necessarily contiguous. Caller DP has n words. Empty or invalid input returns zero.

## C contract and variants

```c
uint32_t pat_alg_lis_001(const int32_t *a, uint32_t n, uint32_t *dp);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Set each subsequence length to one.
2. Compare all earlier smaller elements.
3. Retain longest predecessor extension.

## Worked trace

[3,1,2,5]: subsequence [1,2,5] has length 3.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_lis_001 | const int32_t *a | R0 |
| pat_alg_lis_001 | uint32_t n | R1 |
| pat_alg_lis_001 | uint32_t *dp | R2 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n^2) time, O(n) length space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {3, 1, 2, 5};
  uint32_t d[4];
  return pat_alg_lis_001(a, 4, d) == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {2, 2, 2};
  uint32_t d[3];
  return pat_alg_lis_001(a, 0, d) == 0 && pat_alg_lis_001(a, 3, d) == 1;
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

# PAT-ALG-REDUCTION-001: Signed min max and sum reduction

## Recognition phrases

Nonempty signed/unsigned word scans return status and a result struct with minimum,maximum and 64-bit sum. Result storage is disjoint from input. Both signed and unsigned variants have matching assembly.

## C contract and variants

```c
int pat_alg_reduction_001(const int32_t *values, uint32_t count, pat_alg_reduction_001_signed_result_t *result);
int pat_alg_reduction_001_unsigned( const uint32_t *values, uint32_t count, pat_alg_reduction_001_unsigned_result_t *result);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Initialize min/max from first element and sum from zero.
2. Scan once.
3. Update signed comparisons.
4. Accumulate widened sum.

## Worked trace

[-2,7,1] -> minimum -2,maximum 7,sum 6.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_reduction_001 | const int32_t *values | R0 |
| pat_alg_reduction_001 | uint32_t count | R1 |
| pat_alg_reduction_001 | pat_alg_reduction_001_signed_result_t *result | R2 |
| pat_alg_reduction_001_unsigned | const uint32_t *values | R0 |
| pat_alg_reduction_001_unsigned | uint32_t count | R1 |
| pat_alg_reduction_001_unsigned | pat_alg_reduction_001_unsigned_result_t *result | R2 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) time, O(1) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {-2, 5, 1};
  pat_alg_reduction_001_signed_result_t r;
  return pat_alg_reduction_001(a, 3, &r) && r.minimum == -2 && r.maximum == 5 &&
         r.sum == 4;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {INT32_MIN, INT32_MAX};
  uint32_t u[] = {0, UINT32_MAX};
  pat_alg_reduction_001_signed_result_t s;
  pat_alg_reduction_001_unsigned_result_t r;
  return !pat_alg_reduction_001(NULL, 0, &s) && pat_alg_reduction_001(a, 2, &s) &&
         s.sum == -1 && pat_alg_reduction_001_unsigned(u, 2, &r) && r.sum == UINT32_MAX;
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

# PAT-ALG-PREFIX-SUM-001: Prefix sums and range sums

## Recognition phrases

Signed-word input builds count+1 signed 64-bit prefix values, starting at zero. Range queries use [begin,end) within the count and must use a prefix array built under this contract.

## C contract and variants

```c
int pat_alg_prefix_sum_001(const int32_t *values, uint32_t count, int64_t *prefix);
int pat_alg_prefix_sum_001_range(const int64_t *prefix, uint32_t count, uint32_t begin, uint32_t end, int64_t *sum);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Write prefix[0]=0.
2. Accumulate each element into prefix[i+1].
3. Answer [begin,end) as prefix[end]-prefix[begin].

## Worked trace

[2,-1,4] -> prefix [0,2,1,5]; sum [1,3)=5-2=3.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_prefix_sum_001 | const int32_t *values | R0 |
| pat_alg_prefix_sum_001 | uint32_t count | R1 |
| pat_alg_prefix_sum_001 | int64_t *prefix | R2 |
| pat_alg_prefix_sum_001_range | const int64_t *prefix | R0 |
| pat_alg_prefix_sum_001_range | uint32_t count | R1 |
| pat_alg_prefix_sum_001_range | uint32_t begin | R2 |
| pat_alg_prefix_sum_001_range | uint32_t end | R3 |
| pat_alg_prefix_sum_001_range | int64_t *sum | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) preprocessing, O(1) per range, O(n) prefix output.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {1, -2, 4};
  int64_t p[4];
  pat_alg_prefix_sum_001(a, 3, p);
  return p[0] == 0 && p[1] == 1 && p[2] == -1 && p[3] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, -2, 4};
  int64_t p[4], s = 0;
  return pat_alg_prefix_sum_001(NULL, 0, p) && pat_alg_prefix_sum_001(a, 3, p) &&
         pat_alg_prefix_sum_001_range(p, 3, 1, 3, &s) && s == 2 &&
         !pat_alg_prefix_sum_001_range(p, 3, 3, 2, &s);
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

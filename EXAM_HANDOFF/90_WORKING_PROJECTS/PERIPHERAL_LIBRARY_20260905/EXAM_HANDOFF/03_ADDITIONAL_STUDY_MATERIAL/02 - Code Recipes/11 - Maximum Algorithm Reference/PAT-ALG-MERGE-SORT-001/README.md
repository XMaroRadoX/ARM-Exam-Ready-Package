# PAT-ALG-MERGE-SORT-001: Stable merge sort

## Recognition phrases

Stable signed-word merge sort. Scratch has n disjoint words; identical buffers are rejected as a no-op. Recursion depth grows logarithmically. The exported ms helper sorts [l,r); require l<=r and both buffers to cover r words. The merge helper requires l<=m<=r and each half already sorted; scratch must be disjoint.

## C contract and variants

```c
void merge(int32_t *a, int32_t *t, uint32_t l, uint32_t m, uint32_t r);
void ms(int32_t *a, int32_t *t, uint32_t l, uint32_t r);
void pat_alg_merge_sort_001(int32_t *a, uint32_t n, int32_t *scratch);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Split half-open range.
2. Recursively sort both halves.
3. Stably merge into scratch.
4. Copy merged range back.

## Worked trace

[3,1,2] splits into [3] and [1,2], then merges into [1,2,3].

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| merge | int32_t *a | R0 |
| merge | int32_t *t | R1 |
| merge | uint32_t l | R2 |
| merge | uint32_t m | R3 |
| merge | uint32_t r | [entry SP] |
| ms | int32_t *a | R0 |
| ms | int32_t *t | R1 |
| ms | uint32_t l | R2 |
| ms | uint32_t r | R3 |
| pat_alg_merge_sort_001 | int32_t *a | R0 |
| pat_alg_merge_sort_001 | uint32_t n | R1 |
| pat_alg_merge_sort_001 | int32_t *scratch | R2 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n log n) time, O(n) caller scratch plus O(log n) recursion.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {3, -1, 2}, t[3];
  pat_alg_merge_sort_001(a, 3, t);
  return a[0] == -1 && a[1] == 2 && a[2] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t halves[] = {1, 3, 2, 4, 987654}, work[5] = {0, 0, 0, 0, 987654};
  merge(halves, work, 0, 2, 4);
  if (halves[0] != 1 || halves[1] != 2 || halves[2] != 3 || halves[3] != 4 ||
      halves[4] != 987654 || work[4] != 987654)
    return 0;
  int32_t a[] = {2, 2, 1}, t[3];
  pat_alg_merge_sort_001(a, 0, t);
  pat_alg_merge_sort_001(a, 3, t);
  return a[0] == 1 && a[1] == 2 && a[2] == 2;
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

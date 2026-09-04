# PAT-ALG-LINEAR-SEARCH-001: Linear search variants

## Recognition phrases

First/last variants return a signed index or -1, so require count<=INT32_MAX. All-matches variant returns total matches while writing at most capacity indexes.

## C contract and variants

```c
int32_t pat_alg_linear_search_001(const int32_t *values, uint32_t count, int32_t key);
int32_t pat_alg_linear_search_001_last(const int32_t *values, uint32_t count, int32_t key);
uint32_t pat_alg_linear_search_001_all(const int32_t *values, uint32_t count, int32_t key, uint32_t *indexes, uint32_t capacity);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Scan forward for first.
2. Scan backward for last.
3. For all matches count every equality and store indexes up to capacity.

## Worked trace

[4,2,4]: first 0,last 2,all [0,2]. Capacity one writes only 0 and still returns 2.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_linear_search_001 | const int32_t *values | R0 |
| pat_alg_linear_search_001 | uint32_t count | R1 |
| pat_alg_linear_search_001 | int32_t key | R2 |
| pat_alg_linear_search_001_last | const int32_t *values | R0 |
| pat_alg_linear_search_001_last | uint32_t count | R1 |
| pat_alg_linear_search_001_last | int32_t key | R2 |
| pat_alg_linear_search_001_all | const int32_t *values | R0 |
| pat_alg_linear_search_001_all | uint32_t count | R1 |
| pat_alg_linear_search_001_all | int32_t key | R2 |
| pat_alg_linear_search_001_all | uint32_t *indexes | R3 |
| pat_alg_linear_search_001_all | uint32_t capacity | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) time, O(1) internal space plus optional index output.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {4, 7, 7};
  return pat_alg_linear_search_001(a, 3, 7) == 1 &&
         pat_alg_linear_search_001(a, 3, 9) == -1;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {5, 5, 2, 5};
  uint32_t out[2] = {9, 9};
  return pat_alg_linear_search_001(a, 0, 5) == -1 &&
         pat_alg_linear_search_001_last(a, 4, 5) == 3 &&
         pat_alg_linear_search_001_all(a, 4, 5, out, 2) == 3 && out[0] == 0 &&
         out[1] == 1;
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

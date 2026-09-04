# PAT-ALG-BUBBLE-SORT-001: Bubble sort with early termination

## Recognition phrases

Stable ascending signed-word sorting in place. Stop early when a pass makes no swaps; null input is a no-op.

## C contract and variants

```c
void pat_alg_bubble_sort_001(int32_t *a, uint32_t n);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Compare adjacent pairs.
2. Swap inversions.
3. Shorten the unsorted suffix.
4. Stop early after a no-swap pass.

## Worked trace

[3,2,1] -> [2,1,3] -> [1,2,3].

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_bubble_sort_001 | int32_t *a | R0 |
| pat_alg_bubble_sort_001 | uint32_t n | R1 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) best and O(n^2) worst time, O(1) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {3, -1, 2};
  pat_alg_bubble_sort_001(a, 3);
  return a[0] == -1 && a[1] == 2 && a[2] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, 2, 3}, b[] = {2, 2, 1};
  pat_alg_bubble_sort_001(a, 3);
  pat_alg_bubble_sort_001(b, 3);
  return a[0] == 1 && a[2] == 3 && b[0] == 1 && b[2] == 2;
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

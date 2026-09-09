# PAT-ALG-COMPONENT-MERGE-001: Component-label merge

## Recognition phrases

Five arguments: labels,count,from,to,limit. Replace matching labels if count<=limit; return number of matches. This is a helper for component merging, not the full seven-argument maze exam.

## C contract and variants

```c
uint32_t pat_alg_component_merge_001(uint32_t *label, uint32_t n, uint32_t from, uint32_t to, uint32_t limit);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Validate label array and limit.
2. Scan n labels.
3. Replace every from label with to.
4. Count replacements.

## Worked trace

[1,2,1], from 1,to 3 -> [3,2,3], return 2.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_component_merge_001 | uint32_t *label | R0 |
| pat_alg_component_merge_001 | uint32_t n | R1 |
| pat_alg_component_merge_001 | uint32_t from | R2 |
| pat_alg_component_merge_001 | uint32_t to | R3 |
| pat_alg_component_merge_001 | uint32_t limit | [entry SP] |


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
  uint32_t a[] = {1, 2, 1};
  return pat_alg_component_merge_001(a, 3, 1, 2, 3) == 2 && a[0] == 2 && a[2] == 2;
}
static int pattern_edge_vectors(void) {
  uint32_t a[] = {1, 1};
  return pat_alg_component_merge_001(a, 2, 1, 2, 1) == 0 &&
         pat_alg_component_merge_001(NULL, 0, 1, 2, 0) == 0;
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

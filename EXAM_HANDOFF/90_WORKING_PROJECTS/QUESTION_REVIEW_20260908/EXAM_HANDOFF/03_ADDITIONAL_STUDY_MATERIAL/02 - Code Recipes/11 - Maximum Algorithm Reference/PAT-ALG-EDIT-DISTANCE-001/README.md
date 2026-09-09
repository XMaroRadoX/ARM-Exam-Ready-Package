# PAT-ALG-EDIT-DISTANCE-001: Edit distance

## Recognition phrases

Explicit string lengths. Two-row version needs separate arrays of second_length+1 words; full version checks table_elements. Return edit count, or UINT32_MAX on rejected input/dimensions.

## C contract and variants

```c
uint32_t pat_alg_edit_distance_001(const char *first, const char *second, uint32_t first_length, uint32_t second_length, uint32_t *previous, uint32_t *current);
uint32_t pat_alg_edit_distance_001_full(const char *first, const char *second, uint32_t first_length, uint32_t second_length, uint32_t *table, uint32_t table_elements);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Initialize first row/column.
2. For each character pair compute delete/insert/substitute.
3. Keep minimum.
4. Use either full table or two rows.

## Worked trace

"cat" to "cut": one substitution, distance 1.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_edit_distance_001 | const char *first | R0 |
| pat_alg_edit_distance_001 | const char *second | R1 |
| pat_alg_edit_distance_001 | uint32_t first_length | R2 |
| pat_alg_edit_distance_001 | uint32_t second_length | R3 |
| pat_alg_edit_distance_001 | uint32_t *previous | [entry SP] |
| pat_alg_edit_distance_001 | uint32_t *current | [entry SP+4] |
| pat_alg_edit_distance_001_full | const char *first | R0 |
| pat_alg_edit_distance_001_full | const char *second | R1 |
| pat_alg_edit_distance_001_full | uint32_t first_length | R2 |
| pat_alg_edit_distance_001_full | uint32_t second_length | R3 |
| pat_alg_edit_distance_001_full | uint32_t *table | [entry SP] |
| pat_alg_edit_distance_001_full | uint32_t table_elements | [entry SP+4] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(a*b) time; O(a*b) full-table or O(b) two-row space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint32_t p[8], c[8];
  return pat_alg_edit_distance_001("kitten", "sitting", 6, 7, p, c) == 3;
}
static int pattern_edge_vectors(void) {
  uint32_t p[4], c[4], t[16];
  return pat_alg_edit_distance_001("", "abc", 0, 3, p, c) == 3 &&
         pat_alg_edit_distance_001("abc", "", 3, 0, p, c) == 3 &&
         pat_alg_edit_distance_001_full("abc", "adc", 3, 3, t, 16) == 1 &&
         pat_alg_edit_distance_001_full("a", "b", 1, 1, t, 3) == UINT32_MAX;
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

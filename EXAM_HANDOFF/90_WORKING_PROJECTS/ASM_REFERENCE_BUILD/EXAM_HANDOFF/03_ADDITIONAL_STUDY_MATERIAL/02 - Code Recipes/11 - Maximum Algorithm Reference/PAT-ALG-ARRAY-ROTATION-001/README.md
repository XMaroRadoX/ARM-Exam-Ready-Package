# PAT-ALG-ARRAY-ROTATION-001: Left and right array rotation

## Recognition phrases

Normalize rotation modulo count. Left/right variants mutate in place; scratch rotation requires disjoint scratch_count>=count.

## C contract and variants

```c
void pat_alg_array_rotation_001(int32_t *values, uint32_t count, uint32_t positions);
void pat_alg_array_rotation_001_right(int32_t *values, uint32_t count, uint32_t positions);
int pat_alg_array_rotation_001_with_scratch(int32_t *values, uint32_t count, uint32_t positions, int32_t *scratch, uint32_t scratch_count);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Normalize k.
2. Reverse the first and second regions.
3. Reverse the whole array.
4. Derive right rotation or use scratch mapping.

## Worked trace

[1,2,3,4], left 1 -> [2,3,4,1]; right 1 -> [4,1,2,3].

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_array_rotation_001 | int32_t *values | R0 |
| pat_alg_array_rotation_001 | uint32_t count | R1 |
| pat_alg_array_rotation_001 | uint32_t positions | R2 |
| pat_alg_array_rotation_001_right | int32_t *values | R0 |
| pat_alg_array_rotation_001_right | uint32_t count | R1 |
| pat_alg_array_rotation_001_right | uint32_t positions | R2 |
| pat_alg_array_rotation_001_with_scratch | int32_t *values | R0 |
| pat_alg_array_rotation_001_with_scratch | uint32_t count | R1 |
| pat_alg_array_rotation_001_with_scratch | uint32_t positions | R2 |
| pat_alg_array_rotation_001_with_scratch | int32_t *scratch | R3 |
| pat_alg_array_rotation_001_with_scratch | uint32_t scratch_count | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) time; O(1) for reversal or O(n) caller scratch.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[] = {1, 2, 3, 4};
  pat_alg_array_rotation_001(a, 4, 2);
  return a[0] == 3 && a[1] == 4 && a[2] == 1 && a[3] == 2;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, 2, 3, 4}, b[] = {1, 2, 3}, t[3];
  pat_alg_array_rotation_001_right(a, 4, 1);
  return a[0] == 4 && a[1] == 1 && a[3] == 3 &&
         pat_alg_array_rotation_001_with_scratch(b, 3, 1, t, 3) && b[0] == 2 &&
         b[2] == 1 && !pat_alg_array_rotation_001_with_scratch(b, 3, 1, t, 2);
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

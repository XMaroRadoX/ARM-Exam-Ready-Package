# PAT-DS-UNION-FIND-001: Union-find with compression and rank

## Recognition phrases

Parent links must form an initialized forest with roots pointing to themselves and valid ranks. The wrapper checks endpoint indexes. The raw find helper assumes valid forest links; corrupt or cyclic input is outside this interface contract.

## C contract and variants

```c
uint32_t find(uint32_t *p, uint32_t x);
int pat_ds_union_find_001(uint32_t *p, uint8_t *r, uint32_t n, uint32_t a, uint32_t b);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Follow parent links with path halving.
2. Find both roots.
3. Attach lower rank under higher.
4. Increment rank on a tie.

## Worked trace

Initially parent [0,1,2]; union(0,1) joins their roots, while 2 remains separate.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| find | uint32_t *p | R0 |
| find | uint32_t x | R1 |
| pat_ds_union_find_001 | uint32_t *p | R0 |
| pat_ds_union_find_001 | uint8_t *r | R1 |
| pat_ds_union_find_001 | uint32_t n | R2 |
| pat_ds_union_find_001 | uint32_t a | R3 |
| pat_ds_union_find_001 | uint32_t b | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

amortized inverse-Ackermann time, O(n) parent/rank space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint32_t p[] = {0, 1, 2};
  uint8_t r[3] = {0};
  return pat_ds_union_find_001(p, r, 3, 0, 1) && find(p, 0) == find(p, 1);
}
static int pattern_edge_vectors(void) {
  uint32_t p[] = {0, 1};
  uint8_t r[2] = {0};
  return pat_ds_union_find_001(p, r, 2, 0, 1) && pat_ds_union_find_001(p, r, 2, 0, 1) &&
         find(p, 0) == find(p, 1) && !pat_ds_union_find_001(p, r, 2, 0, 2);
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

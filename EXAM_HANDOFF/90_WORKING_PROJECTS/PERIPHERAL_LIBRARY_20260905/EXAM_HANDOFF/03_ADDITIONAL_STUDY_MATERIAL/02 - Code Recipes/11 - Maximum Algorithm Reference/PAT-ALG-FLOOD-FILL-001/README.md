# PAT-ALG-FLOOD-FILL-001: Flood fill and maze propagation

## Recognition phrases

Four-neighbor byte grid, dimensions must multiply without overflow. Queue has rows*cols words; old and new colors must differ. Mark cells before enqueue and return recolored count.

## C contract and variants

```c
uint32_t pat_alg_flood_fill_001(uint8_t *g, uint32_t rows, uint32_t cols, uint32_t start, uint8_t oldv, uint8_t newv, uint32_t *q);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Validate start and colors.
2. Recolor when enqueued.
3. Dequeue cells.
4. Enqueue four in-bounds matching neighbors.

## Worked trace

An all-zero 2x2 grid filled from cell zero changes four cells.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_flood_fill_001 | uint8_t *g | R0 |
| pat_alg_flood_fill_001 | uint32_t rows | R1 |
| pat_alg_flood_fill_001 | uint32_t cols | R2 |
| pat_alg_flood_fill_001 | uint32_t start | R3 |
| pat_alg_flood_fill_001 | uint8_t oldv | [entry SP] |
| pat_alg_flood_fill_001 | uint8_t newv | [entry SP+4] |
| pat_alg_flood_fill_001 | uint32_t *q | [entry SP+8] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(rows*cols) time and queue space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint8_t g[] = {1, 1, 0, 1};
  uint32_t q[4];
  return pat_alg_flood_fill_001(g, 2, 2, 0, 1, 2, q) == 3 && g[3] == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t g[] = {1};
  uint32_t q[1];
  return pat_alg_flood_fill_001(g, 1, 1, 0, 1, 2, q) == 1 && g[0] == 2 &&
         pat_alg_flood_fill_001(g, 1, 1, 0, 2, 2, q) == 0 &&
         pat_alg_flood_fill_001(NULL, 1, 1, 0, 1, 2, q) == 0;
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

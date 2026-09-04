# PAT-ALG-KNAPSACK-001: Bounded zero-one knapsack

## Recognition phrases

Zero-one knapsack with unsigned-halfword weights/values, n<=65535. DP has cap+1 words. Traverse capacity downward; each item is used once, including zero-weight items. Invalid input returns zero.

## C contract and variants

```c
uint32_t pat_alg_knapsack_001(const uint16_t *wt, const uint16_t *val, uint32_t n, uint32_t cap, uint32_t *dp);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Zero capacity table.
2. For each item traverse capacities downward.
3. Compare skip versus take value.

## Worked trace

One item weight 2,value 3, capacity 4 -> value 3, not 6.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_knapsack_001 | const uint16_t *wt | R0 |
| pat_alg_knapsack_001 | const uint16_t *val | R1 |
| pat_alg_knapsack_001 | uint32_t n | R2 |
| pat_alg_knapsack_001 | uint32_t cap | R3 |
| pat_alg_knapsack_001 | uint32_t *dp | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(items*capacity) time, O(capacity) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint16_t w[] = {2, 3}, v[] = {3, 4};
  uint32_t d[4];
  return pat_alg_knapsack_001(w, v, 2, 3, d) == 4;
}
static int pattern_edge_vectors(void) {
  uint16_t w[] = {1}, v[] = {2};
  uint32_t d[2];
  return pat_alg_knapsack_001(w, v, 0, 1, d) == 0 &&
         pat_alg_knapsack_001(w, v, 1, 0, d) == 0 &&
         pat_alg_knapsack_001(w, v, 1, 1, d) == 2;
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

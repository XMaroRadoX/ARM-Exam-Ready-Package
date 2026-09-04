# PAT-ALG-DIJKSTRA-001: Dijkstra shortest path

## Recognition phrases

Nonnegative unsigned matrix weights; zero means no edge. n<=32767; dist and done hold n elements. UINT32_MAX is reserved for unreachable/unrepresentable distances. Checked addition prevents wrapping a path into a smaller one.

## C contract and variants

```c
int pat_alg_dijkstra_001(const uint32_t *w, uint32_t n, uint32_t start, uint32_t *dist, uint8_t *done);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Initialize infinity/start.
2. Repeatedly choose unfinished minimum-distance vertex.
3. Relax nonnegative outgoing edges with overflow guard.

## Worked trace

Edges 0->1=2,1->2=3,0->2=9 yield distances [0,2,5].

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_dijkstra_001 | const uint32_t *w | R0 |
| pat_alg_dijkstra_001 | uint32_t n | R1 |
| pat_alg_dijkstra_001 | uint32_t start | R2 |
| pat_alg_dijkstra_001 | uint32_t *dist | R3 |
| pat_alg_dijkstra_001 | uint8_t *done | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(V^2) time, O(V) distance/finished space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint32_t w[9] = {0, 2, 9, 0, 0, 3, 0, 0, 0}, d[3];
  uint8_t done[3];
  return pat_alg_dijkstra_001(w, 3, 0, d, done) && d[2] == 5;
}
static int pattern_edge_vectors(void) {
  uint32_t w[1] = {0}, d[1];
  uint8_t done[1];
  return pat_alg_dijkstra_001(w, 1, 0, d, done) && d[0] == 0 &&
         !pat_alg_dijkstra_001(w, 1, 1, d, done) &&
         !pat_alg_dijkstra_001(NULL, 1, 0, d, done);
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

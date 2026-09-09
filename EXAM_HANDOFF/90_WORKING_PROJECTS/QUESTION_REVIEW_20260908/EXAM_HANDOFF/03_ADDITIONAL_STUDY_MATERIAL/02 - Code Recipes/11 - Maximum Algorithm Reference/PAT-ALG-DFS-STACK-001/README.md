# PAT-ALG-DFS-STACK-001: Bounded DFS with an explicit stack

## Recognition phrases

Byte adjacency matrix, n<=65535, zero-initialized seen and n-word stack. Mark on push, so each vertex is pending at most once. Return newly visited count; an already-seen start returns zero.

## C contract and variants

```c
uint32_t pat_alg_dfs_stack_001(const uint8_t *adj, uint32_t n, uint32_t start, uint8_t *seen, uint32_t *stack);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Validate buffers/start.
2. Push start.
3. Pop until empty.
4. Skip visited nodes.
5. Mark and count.
6. Push bounded unseen neighbors.

## Worked trace

A complete six-vertex graph visits six vertices without requiring more than six stack entries.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_dfs_stack_001 | const uint8_t *adj | R0 |
| pat_alg_dfs_stack_001 | uint32_t n | R1 |
| pat_alg_dfs_stack_001 | uint32_t start | R2 |
| pat_alg_dfs_stack_001 | uint8_t *seen | R3 |
| pat_alg_dfs_stack_001 | uint32_t *stack | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(V^2) time for an adjacency matrix, O(V) caller-provided stack/seen space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint8_t a[9] = {0, 1, 0, 1, 0, 1, 0, 1, 0}, s[3] = {0};
  uint32_t q[3];
  return pat_alg_dfs_stack_001(a, 3, 0, s, q) == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t dense[36], seen2[6] = {0};
  uint32_t stack2[7] = {0};
  for (unsigned z = 0; z < 36; z++)
    dense[z] = 1;
  stack2[6] = 77;
  if (pat_alg_dfs_stack_001(dense, 6, 0, seen2, stack2) != 6 || stack2[6] != 77)
    return 0;
  uint8_t a[1] = {0}, s[1] = {0};
  uint32_t q[1];
  return pat_alg_dfs_stack_001(a, 1, 0, s, q) == 1 &&
         pat_alg_dfs_stack_001(NULL, 1, 0, s, q) == 0 &&
         pat_alg_dfs_stack_001(a, 1, 1, s, q) == 0;
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

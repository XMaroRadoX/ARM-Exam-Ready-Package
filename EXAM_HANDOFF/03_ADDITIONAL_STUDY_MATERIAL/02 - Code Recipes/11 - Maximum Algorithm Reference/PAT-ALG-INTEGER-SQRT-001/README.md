# PAT-ALG-INTEGER-SQRT-001: Integer square root

## Recognition phrases

Unsigned integer square root rounded down; no floating-point operations.

## C contract and variants

```c
uint32_t pat_alg_integer_sqrt_001(uint32_t n);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Start at highest power-of-four bit.
2. Test subtract candidate.
3. Update partial root.
4. Shift bit by two.

## Worked trace

sqrt(15) -> 3; sqrt(16) -> 4; UINT32_MAX -> 65535.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_integer_sqrt_001 | uint32_t n | R0 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(word bits) time, O(1) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  return pat_alg_integer_sqrt_001(0) == 0 && pat_alg_integer_sqrt_001(15) == 3 &&
         pat_alg_integer_sqrt_001(16) == 4;
}
static int pattern_edge_vectors(void) {
  return pat_alg_integer_sqrt_001(1) == 1 &&
         pat_alg_integer_sqrt_001(UINT32_MAX) == 65535u;
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

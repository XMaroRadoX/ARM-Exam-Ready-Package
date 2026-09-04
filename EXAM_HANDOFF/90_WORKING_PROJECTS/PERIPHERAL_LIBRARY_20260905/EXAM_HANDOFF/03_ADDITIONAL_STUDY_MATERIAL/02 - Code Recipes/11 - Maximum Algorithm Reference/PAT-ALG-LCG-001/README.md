# PAT-ALG-LCG-001: Five-argument linear congruential generator

## Recognition phrases

Five arguments: x,a,c,m,shift. First compute a*x+c modulo 2^32, then optional modulus, then right shift. shift>=32 returns zero.

## C contract and variants

```c
uint32_t pat_alg_lcg_001(uint32_t x, uint32_t a, uint32_t c, uint32_t m, uint32_t shift);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Compute a*x+c with 32-bit wraparound.
2. Apply modulus when nonzero.
3. Shift only when shift is below 32.
4. Return result.

## Worked trace

x=3,a=5,c=1,m=16,shift=0 -> (16 mod 16)=0.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_lcg_001 | uint32_t x | R0 |
| pat_alg_lcg_001 | uint32_t a | R1 |
| pat_alg_lcg_001 | uint32_t c | R2 |
| pat_alg_lcg_001 | uint32_t m | R3 |
| pat_alg_lcg_001 | uint32_t shift | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(1) time and space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) { return pat_alg_lcg_001(1, 5, 3, 7, 0) == 1; }
static int pattern_edge_vectors(void) {
  return pat_alg_lcg_001(1, 1, 1, 0, 0) == 2 && pat_alg_lcg_001(1, 1, 1, 7, 32) == 0;
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

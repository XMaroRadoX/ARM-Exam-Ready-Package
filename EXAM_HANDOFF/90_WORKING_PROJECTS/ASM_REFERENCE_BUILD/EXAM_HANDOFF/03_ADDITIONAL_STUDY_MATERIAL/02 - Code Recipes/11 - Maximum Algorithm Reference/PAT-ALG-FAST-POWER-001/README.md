# PAT-ALG-FAST-POWER-001: Exponentiation by squaring

## Recognition phrases

Primary computes exponentiation by squaring; nonzero modulus gives modular arithmetic, modulus zero gives modulo-2^32 arithmetic. Checked variant returns status and leaves output unchanged on overflow.

## C contract and variants

```c
uint32_t pat_alg_fast_power_001(uint32_t base, uint32_t exponent, uint32_t modulus);
int pat_alg_fast_power_001_checked(uint32_t base, uint32_t exponent, uint32_t *result);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Maintain accumulated result and squared factor.
2. Multiply on set exponent bits.
3. Square and shift exponent.
4. Optionally reduce modulo.

## Worked trace

3^5=243; modulo 7 gives 5.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_fast_power_001 | uint32_t base | R0 |
| pat_alg_fast_power_001 | uint32_t exponent | R1 |
| pat_alg_fast_power_001 | uint32_t modulus | R2 |
| pat_alg_fast_power_001_checked | uint32_t base | R0 |
| pat_alg_fast_power_001_checked | uint32_t exponent | R1 |
| pat_alg_fast_power_001_checked | uint32_t *result | R2 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(log exponent) time, O(1) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) { return pat_alg_fast_power_001(3, 4, 5) == 1; }
static int pattern_edge_vectors(void) {
  uint32_t out = 0;
  return pat_alg_fast_power_001(7, 0, 5) == 1 &&
         pat_alg_fast_power_001_checked(3, 4, &out) && out == 81 &&
         !pat_alg_fast_power_001_checked(UINT32_MAX, 2, &out);
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

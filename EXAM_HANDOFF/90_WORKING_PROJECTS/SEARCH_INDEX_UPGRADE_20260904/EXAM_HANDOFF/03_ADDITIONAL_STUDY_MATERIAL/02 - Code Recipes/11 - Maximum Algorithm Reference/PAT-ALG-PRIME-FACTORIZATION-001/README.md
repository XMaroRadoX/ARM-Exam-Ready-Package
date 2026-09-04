# PAT-ALG-PRIME-FACTORIZATION-001: Prime testing and trial factorization

## Recognition phrases

Primary tests primality; factorize emits ascending prime factors and returns total count even when capacity truncates writes. Zero and one have no factors.

## C contract and variants

```c
int pat_alg_prime_factorization_001(uint32_t value);
uint32_t pat_alg_prime_factorization_001_factorize(uint32_t value, uint32_t *factors, uint32_t capacity);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Reject values below two.
2. Handle two/even values.
3. Try odd divisors through n/divisor.
4. Repeatedly divide to factorize.

## Worked trace

36 -> factors 2,2,3,3; count 4.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_prime_factorization_001 | uint32_t value | R0 |
| pat_alg_prime_factorization_001_factorize | uint32_t value | R0 |
| pat_alg_prime_factorization_001_factorize | uint32_t *factors | R1 |
| pat_alg_prime_factorization_001_factorize | uint32_t capacity | R2 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(sqrt n) trial time; O(number of factors) output.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  return pat_alg_prime_factorization_001(29) && !pat_alg_prime_factorization_001(21) &&
         !pat_alg_prime_factorization_001(1);
}
static int pattern_edge_vectors(void) {
  uint32_t f[4] = {0};
  return pat_alg_prime_factorization_001(2) && !pat_alg_prime_factorization_001(0) &&
         pat_alg_prime_factorization_001_factorize(12, f, 4) == 3 && f[0] == 2 &&
         f[1] == 2 && f[2] == 3 &&
         pat_alg_prime_factorization_001_factorize(1, f, 4) == 0;
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

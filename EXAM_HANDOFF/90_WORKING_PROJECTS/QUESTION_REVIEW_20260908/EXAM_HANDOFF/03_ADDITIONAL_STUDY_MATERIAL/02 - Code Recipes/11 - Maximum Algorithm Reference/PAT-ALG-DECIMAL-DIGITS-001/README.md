# PAT-ALG-DECIMAL-DIGITS-001: Decimal digit algorithms

## Recognition phrases

Primary packs digit sum and the low 16 bits of decimal reversal; it is not a full reversal API. The palindrome variant compares a full widened reversal. Extraction writes least-significant digits first and may leave a prefix on insufficient capacity. Legacy reconstruction wraps modulo 2^32; digits must be 0..9. Kaprekar operates on the low four decimal digits.

## C contract and variants

```c
uint32_t pat_alg_decimal_digits_001(uint32_t value);
uint32_t pat_alg_decimal_digits_001_extract(uint32_t value, uint8_t *digits, uint32_t capacity);
uint32_t pat_alg_decimal_digits_001_reconstruct(const uint8_t *digits, uint32_t count);
int pat_alg_decimal_digits_001_is_palindrome(uint32_t value);
uint32_t pat_alg_decimal_digits_001_kaprekar_4(uint32_t value);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Extract base-10 digits with remainder/division.
2. Reconstruct in reverse order.
3. Compare for palindrome.
4. Sort four digits for Kaprekar step.

## Worked trace

123321 reverses to 123321, so palindrome=true; it must not be compared with only 57785.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_decimal_digits_001 | uint32_t value | R0 |
| pat_alg_decimal_digits_001_extract | uint32_t value | R0 |
| pat_alg_decimal_digits_001_extract | uint8_t *digits | R1 |
| pat_alg_decimal_digits_001_extract | uint32_t capacity | R2 |
| pat_alg_decimal_digits_001_reconstruct | const uint8_t *digits | R0 |
| pat_alg_decimal_digits_001_reconstruct | uint32_t count | R1 |
| pat_alg_decimal_digits_001_is_palindrome | uint32_t value | R0 |
| pat_alg_decimal_digits_001_kaprekar_4 | uint32_t value | R0 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(number of digits), except fixed four-digit Kaprekar sorting.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  return pat_alg_decimal_digits_001(123) == ((6u << 16) | 321u);
}
static int pattern_edge_vectors(void) {
  if (!pat_alg_decimal_digits_001_is_palindrome(123321u) ||
      !pat_alg_decimal_digits_001_is_palindrome(4000000004u) ||
      pat_alg_decimal_digits_001_is_palindrome(UINT32_MAX))
    return 0;
  uint8_t d[10];
  uint32_t n = pat_alg_decimal_digits_001_extract(1203, d, 10);
  return n == 4 && pat_alg_decimal_digits_001_reconstruct(d, n) == 1203 &&
         pat_alg_decimal_digits_001_is_palindrome(1221) &&
         !pat_alg_decimal_digits_001_is_palindrome(123) &&
         pat_alg_decimal_digits_001_kaprekar_4(3524) == 3087;
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

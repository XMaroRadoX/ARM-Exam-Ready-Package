# PAT-ALG-HORNER-001: Horner polynomial evaluation

## Recognition phrases

Coefficients are stored from constant term upward. Legacy result uses defined 64-bit two-complement wraparound; null input returns zero. The checked variant returns status, rejects intermediate overflow and leaves output unchanged on failure.

## C contract and variants

```c
int64_t pat_alg_horner_001(const int32_t *c, uint32_t n, int32_t x);
int pat_alg_horner_001_checked(const int32_t *c, uint32_t n, int32_t x, int64_t *out);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Start at zero.
2. Consume coefficients from highest degree.
3. Multiply accumulator by x and add next coefficient.

## Worked trace

Coefficients [1,2,3], x=2: ((3*2)+2)*2+1=17.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_horner_001 | const int32_t *c | R0 |
| pat_alg_horner_001 | uint32_t n | R1 |
| pat_alg_horner_001 | int32_t x | R2 |
| pat_alg_horner_001_checked | const int32_t *c | R0 |
| pat_alg_horner_001_checked | uint32_t n | R1 |
| pat_alg_horner_001_checked | int32_t x | R2 |
| pat_alg_horner_001_checked | int64_t *out | R3 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) time, O(1) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t c[] = {1, 2};
  return pat_alg_horner_001(c, 2, 3) == 7;
}
static int pattern_edge_vectors(void) {
  int64_t checked = 99;
  int32_t ok_poly[3] = {1, 2, 3}, overflow_poly[4] = {0, 0, 0, INT32_MAX};
  if (!pat_alg_horner_001_checked(ok_poly, 3, 2, &checked) || checked != 17)
    return 0;
  checked = 99;
  if (pat_alg_horner_001_checked(overflow_poly, 4, INT32_MAX, &checked) ||
      checked != 99)
    return 0;
  if (pat_alg_horner_001(NULL, 3, 2) != 0)
    return 0;
  int32_t c[] = {5};
  return pat_alg_horner_001(c, 0, 7) == 0 && pat_alg_horner_001(c, 1, 7) == 5;
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

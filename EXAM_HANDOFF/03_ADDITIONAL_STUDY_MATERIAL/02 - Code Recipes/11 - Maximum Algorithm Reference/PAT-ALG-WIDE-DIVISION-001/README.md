# PAT-ALG-WIDE-DIVISION-001: Signed 64-by-32 restoring division

## Recognition phrases

Signed 64-by-32 division truncates toward zero; remainder has dividend sign. Divisor zero returns zero and writes zero remainder. INT64_MIN/-1 retains the legacy INT64_MIN bit-pattern result and must be treated as overflow by callers.

## C contract and variants

```c
int64_t pat_alg_wide_division_001(int64_t dividend, int32_t divisor, int32_t *remainder);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Reject zero divisor.
2. Normalize signs.
3. Repeat 64 shift/compare/subtract steps.
4. Restore quotient and remainder signs.
5. Return R0:R1.

## Worked trace

-17/5 -> quotient -3, remainder -2.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_wide_division_001 | int64_t dividend | R0:R1 |
| pat_alg_wide_division_001 | int32_t divisor | R2 |
| pat_alg_wide_division_001 | int32_t *remainder | R3 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(64) time for fixed widths, O(1) space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t r = 0;
  return pat_alg_wide_division_001(-15, 2, &r) == -7 && r == -1;
}
static int pattern_edge_vectors(void) {
  int32_t rem_limit = 99;
  if (pat_alg_wide_division_001(INT64_MIN, 1, &rem_limit) != INT64_MIN ||
      rem_limit != 0 ||
      pat_alg_wide_division_001(INT64_MIN, -1, &rem_limit) != INT64_MIN)
    return 0;
  int32_t r = 7;
  return pat_alg_wide_division_001(0, 5, &r) == 0 && r == 0 &&
         pat_alg_wide_division_001(15, -2, &r) == -7 && r == 1 &&
         pat_alg_wide_division_001(9, 0, &r) == 0 && r == 0;
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

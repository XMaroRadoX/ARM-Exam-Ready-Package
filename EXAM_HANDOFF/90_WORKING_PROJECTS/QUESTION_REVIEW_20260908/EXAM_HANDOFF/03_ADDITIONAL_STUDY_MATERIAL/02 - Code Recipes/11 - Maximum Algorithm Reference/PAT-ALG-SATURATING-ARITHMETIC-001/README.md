# PAT-ALG-SATURATING-ARITHMETIC-001: Clamp absolute saturation and overflow

## Recognition phrases

Clamp signed 64-bit values into chosen signed-word limits. Reversed limits return minimum. Absolute INT32_MIN is returned as unsigned 2147483648; signed addition saturates.

## C contract and variants

```c
int32_t pat_alg_saturating_arithmetic_001(int64_t value, int32_t minimum, int32_t maximum);
uint32_t pat_alg_saturating_arithmetic_001_abs_i32(int32_t value);
int32_t pat_alg_saturating_arithmetic_001_add_i32(int32_t first, int32_t second);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Compare widened value to bounds.
2. Clamp outside values.
3. Compute absolute through int64.
4. Use widened addition before saturation.

## Worked trace

INT32_MAX+1 saturates to INT32_MAX.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_saturating_arithmetic_001 | int64_t value | R0:R1 |
| pat_alg_saturating_arithmetic_001 | int32_t minimum | R2 |
| pat_alg_saturating_arithmetic_001 | int32_t maximum | R3 |
| pat_alg_saturating_arithmetic_001_abs_i32 | int32_t value | R0 |
| pat_alg_saturating_arithmetic_001_add_i32 | int32_t first | R0 |
| pat_alg_saturating_arithmetic_001_add_i32 | int32_t second | R1 |


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
static int pattern_core_vector(void) {
  return pat_alg_saturating_arithmetic_001(50, 0, 10) == 10 &&
         pat_alg_saturating_arithmetic_001(-2, 0, 10) == 0;
}
static int pattern_edge_vectors(void) {
  return pat_alg_saturating_arithmetic_001(5, 10, 0) == 10 &&
         pat_alg_saturating_arithmetic_001_abs_i32(INT32_MIN) == UINT32_C(2147483648) &&
         pat_alg_saturating_arithmetic_001_add_i32(INT32_MAX, 1) == INT32_MAX &&
         pat_alg_saturating_arithmetic_001_add_i32(INT32_MIN, -1) == INT32_MIN;
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

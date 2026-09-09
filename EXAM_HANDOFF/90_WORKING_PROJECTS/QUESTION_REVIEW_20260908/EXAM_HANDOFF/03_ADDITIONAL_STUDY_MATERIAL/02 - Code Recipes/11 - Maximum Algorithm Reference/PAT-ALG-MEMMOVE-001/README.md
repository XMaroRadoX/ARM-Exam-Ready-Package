# PAT-ALG-MEMMOVE-001: Overlap-safe memory movement

## Recognition phrases

Overlap-safe byte movement using integer address ordering. Return destination. Null inputs are a no-op; valid spans must contain n accessible bytes.

## C contract and variants

```c
void *pat_alg_memmove_001(void *d, const void *s, uint32_t n);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Compare source/destination ranges.
2. Copy forward when destination precedes source.
3. Otherwise copy backward.

## Worked trace

Move "abcd" one byte right inside its buffer -> "aabcd".

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_memmove_001 | void *d | R0 |
| pat_alg_memmove_001 | const void *s | R1 |
| pat_alg_memmove_001 | uint32_t n | R2 |


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
  char a[6] = "abcd";
  pat_alg_memmove_001(a + 1, a, 4);
  return a[0] == 'a' && a[1] == 'a' && a[4] == 'd';
}
static int pattern_edge_vectors(void) {
  char a[6] = "abcd";
  pat_alg_memmove_001(a, a, 4);
  pat_alg_memmove_001(a, a + 1, 3);
  return a[0] == 'b' && a[2] == 'd';
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

# PAT-ALG-RUN-LENGTH-001: Run-length encoding

## Recognition phrases

Encode byte values into separate value/run arrays with capacity entries. Runs longer than 255 are split. Return entry count, or zero on failure with a possible output prefix.

## C contract and variants

```c
uint32_t pat_alg_run_length_001(const uint8_t *in, uint32_t n, uint8_t *value, uint8_t *run, uint32_t cap);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Start at first unconsumed byte.
2. Count equal bytes up to 255.
3. Verify output capacity.
4. Emit value/count.
5. Repeat including final run.

## Worked trace

256 repeated A bytes -> values [A,A], runs [255,1].

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_run_length_001 | const uint8_t *in | R0 |
| pat_alg_run_length_001 | uint32_t n | R1 |
| pat_alg_run_length_001 | uint8_t *value | R2 |
| pat_alg_run_length_001 | uint8_t *run | R3 |
| pat_alg_run_length_001 | uint32_t cap | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) time, O(1) internal space plus output.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint8_t a[] = {1, 1, 2}, v[3] = {0}, r[3] = {0};
  return pat_alg_run_length_001(a, 3, v, r, 3) == 2 && v[0] == 1 && r[0] == 2 &&
         v[1] == 2 && r[1] == 1;
}
static int pattern_edge_vectors(void) {
  uint8_t v[2], r[2], a[] = {9};
  return pat_alg_run_length_001(a, 0, v, r, 2) == 0 &&
         pat_alg_run_length_001(a, 1, v, r, 2) == 1 && v[0] == 9 && r[0] == 1 &&
         pat_alg_run_length_001(a, 1, v, r, 0) == 0;
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

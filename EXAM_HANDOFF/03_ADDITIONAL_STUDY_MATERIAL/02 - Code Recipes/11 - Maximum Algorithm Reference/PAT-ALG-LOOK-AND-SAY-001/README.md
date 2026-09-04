# PAT-ALG-LOOK-AND-SAY-001: Bounded look-and-say generation

## Recognition phrases

Encode equal-byte runs as (count,value) byte pairs. A run above 255 or insufficient capacity returns zero; a prefix may already be written. Input/output must not overlap.

## C contract and variants

```c
uint32_t pat_alg_look_and_say_001(const uint8_t *in, uint32_t n, uint8_t *out, uint32_t cap);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Count each run.
2. Reject counts above 255.
3. Reserve two output bytes.
4. Emit count then value.
5. Repeat.

## Worked trace

[1,1,2] -> [(2,1),(1,2)], four output bytes.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_look_and_say_001 | const uint8_t *in | R0 |
| pat_alg_look_and_say_001 | uint32_t n | R1 |
| pat_alg_look_and_say_001 | uint8_t *out | R2 |
| pat_alg_look_and_say_001 | uint32_t cap | R3 |


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
  uint8_t a[] = {1, 1, 2}, o[6] = {0};
  return pat_alg_look_and_say_001(a, 3, o, 6) == 4 && o[0] == 2 && o[1] == 1 &&
         o[2] == 1 && o[3] == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {7}, o[2];
  return pat_alg_look_and_say_001(a, 0, o, 2) == 0 &&
         pat_alg_look_and_say_001(a, 1, o, 2) == 2 && o[0] == 1 && o[1] == 7 &&
         pat_alg_look_and_say_001(a, 1, o, 1) == 0;
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

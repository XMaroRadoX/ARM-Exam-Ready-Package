# PAT-ALG-CONSUME-ONCE-MATCH-001: Consume-once duplicate-safe matching

## Recognition phrases

At most 32 bytes per guess/secret. Return exact-position matches and write misplaced matches through cows. Consume duplicate occurrences once.

## C contract and variants

```c
uint32_t pat_alg_consume_once_match_001(const uint8_t *secret, const uint8_t *guess, uint32_t n, uint32_t *cows);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Mark exact matches in two used arrays.
2. For each unused guess scan unused secrets.
3. Consume the first equal value.
4. Return bulls and cows.

## Worked trace

Secret [1,1], guess [1,2]: one bull, zero cows.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_consume_once_match_001 | const uint8_t *secret | R0 |
| pat_alg_consume_once_match_001 | const uint8_t *guess | R1 |
| pat_alg_consume_once_match_001 | uint32_t n | R2 |
| pat_alg_consume_once_match_001 | uint32_t *cows | R3 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n^2) time, O(n) bounded used-marker space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint8_t s[] = {1, 1, 2, 3}, g[] = {1, 2, 1, 4};
  uint32_t c = 0;
  return pat_alg_consume_once_match_001(s, g, 4, &c) == 1 && c == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {1}, b[] = {2};
  uint32_t c = 9;
  return pat_alg_consume_once_match_001(a, b, 0, &c) == 0 && c == 0 &&
         pat_alg_consume_once_match_001(a, b, 1, &c) == 0 && c == 0 &&
         pat_alg_consume_once_match_001(a, b, 33, &c) == 0;
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

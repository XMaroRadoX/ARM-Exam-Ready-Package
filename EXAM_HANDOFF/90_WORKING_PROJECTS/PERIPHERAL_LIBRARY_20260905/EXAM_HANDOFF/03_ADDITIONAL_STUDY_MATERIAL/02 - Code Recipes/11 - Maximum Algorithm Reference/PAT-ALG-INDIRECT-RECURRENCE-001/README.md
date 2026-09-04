# PAT-ALG-INDIRECT-RECURRENCE-001: Indirect-index recurrence

## Recognition phrases

Primary generates Recaman terms beginning 0, using a subtraction only if nonnegative and unused; fallback addition overflow returns zero with a partial prefix. Hofstadter Q begins 1,1; its computed predecessor indexes and addition are checked. A failed Q generation may leave a prefix.

## C contract and variants

```c
uint32_t pat_alg_indirect_recurrence_001(uint32_t *output, uint32_t count);
uint32_t pat_alg_indirect_recurrence_001_hofstadter_q(uint32_t *output,uint32_t count);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Seed sequence.
2. Propose previous-index subtraction.
3. Scan earlier terms for duplicates.
4. Otherwise add index.
5. Store term.

## Worked trace

Recaman: 0,1,3,6,2,7; Hofstadter Q: 1,1,2,3,3.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Handwritten Cortex-M3 Thumb reference.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_indirect_recurrence_001 | uint32_t *output | R0 |
| pat_alg_indirect_recurrence_001 | uint32_t count | R1 |
| pat_alg_indirect_recurrence_001_hofstadter_q | uint32_t *output | R0 |
| pat_alg_indirect_recurrence_001_hofstadter_q | uint32_t count | R1 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n^2) time for duplicate scans, O(n) output space; Hofstadter Q is O(n).

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  uint32_t a[4];
  return pat_alg_indirect_recurrence_001(a, 4) == 4 && a[0] == 0 && a[1] == 1 &&
         a[2] == 3 && a[3] == 6;
}
static int pattern_edge_vectors(void) {
  uint32_t a[8], q[8];
  return pat_alg_indirect_recurrence_001(NULL, 1) == 0 &&
         pat_alg_indirect_recurrence_001(a, 1) == 1 && a[0] == 0 &&
         pat_alg_indirect_recurrence_001_hofstadter_q(q, 6) == 6 && q[5] == 4;
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

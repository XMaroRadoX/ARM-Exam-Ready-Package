# PAT-DS-STACK-001: Array-backed stack

## Recognition phrases

top is a count in [0,cap]. Reject invalid state before access; push fails when full and pop when empty. Return 1 only for a completed operation.

## C contract and variants

```c
int pat_ds_stack_001(int32_t *a, uint32_t cap, uint32_t *top, int push, int32_t *value);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Reject invalid/full/empty state.
2. Push at top then increment.
3. Pop by decrement then load.

## Worked trace

Push 4 then 5; pop returns 5 and decrements top.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_ds_stack_001 | int32_t *a | R0 |
| pat_ds_stack_001 | uint32_t cap | R1 |
| pat_ds_stack_001 | uint32_t *top | R2 |
| pat_ds_stack_001 | int push | R3 |
| pat_ds_stack_001 | int32_t *value | [entry SP] |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(1) per operation, O(capacity) caller storage.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  int32_t a[2], v = 7, o = 0;
  uint32_t top = 0;
  return pat_ds_stack_001(a, 2, &top, 1, &v) && pat_ds_stack_001(a, 2, &top, 0, &o) &&
         o == 7;
}
static int pattern_edge_vectors(void) {
  int32_t guarded[1] = {7}, v_bad = 9;
  uint32_t top_bad = 2;
  if (pat_ds_stack_001(guarded, 1, &top_bad, 0, &v_bad) || v_bad != 9)
    return 0;
  int32_t a[1], v = 1, o = 0;
  uint32_t top = 0;
  return !pat_ds_stack_001(a, 1, &top, 0, &o) && pat_ds_stack_001(a, 1, &top, 1, &v) &&
         !pat_ds_stack_001(a, 1, &top, 1, &v) && pat_ds_stack_001(a, 1, &top, 0, &o) &&
         o == 1;
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

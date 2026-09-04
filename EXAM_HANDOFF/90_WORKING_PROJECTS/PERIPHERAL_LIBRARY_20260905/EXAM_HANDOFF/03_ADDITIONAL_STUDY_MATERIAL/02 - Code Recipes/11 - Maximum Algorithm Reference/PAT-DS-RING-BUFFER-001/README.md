# PAT-DS-RING-BUFFER-001: Circular ring buffer

## Recognition phrases

Caller initializes a valid ring. head is producer index, tail is consumer; validate indexes/count. This reference is not independently interrupt-safe: shared operations require caller synchronization.

## C contract and variants

```c
int pat_ds_ring_buffer_001(ring_t *q, int put, int32_t *value);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Reject invalid/full/empty state.
2. Insert at head or remove at tail.
3. Wrap index modulo capacity.
4. Adjust count.

## Worked trace

Capacity two: put 4,5; take 4; put 6; remaining order 5,6.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_ds_ring_buffer_001 | ring_t *q | R0 |
| pat_ds_ring_buffer_001 | int put | R1 |
| pat_ds_ring_buffer_001 | int32_t *value | R2 |


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
  int32_t b[2], v = 7, o = 0;
  ring_t q = {b, 2, 0, 0, 0};
  return pat_ds_ring_buffer_001(&q, 1, &v) && pat_ds_ring_buffer_001(&q, 0, &o) &&
         o == 7;
}
static int pattern_edge_vectors(void) {
  int32_t guard_data[2] = {7, 8}, guard_value = 9;
  ring_t badq = {guard_data, 2, 2, 0, 0};
  if (pat_ds_ring_buffer_001(&badq, 1, &guard_value) || guard_data[0] != 7)
    return 0;
  int32_t b[1], v = 1, o = 0;
  ring_t q = {b, 1, 0, 0, 0};
  return !pat_ds_ring_buffer_001(&q, 0, &o) && pat_ds_ring_buffer_001(&q, 1, &v) &&
         !pat_ds_ring_buffer_001(&q, 1, &v) && pat_ds_ring_buffer_001(&q, 0, &o) &&
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

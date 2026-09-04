# PAT-DS-LINKED-LIST-001: Singly linked-list operations

## Recognition phrases

Caller supplies an acyclic singly linked list. Find/remove first matching value; inserted node must be detached and distinct from position. Removal detaches the returned node.

## C contract and variants

```c
pat_ds_linked_list_001_node_t * pat_ds_linked_list_001(pat_ds_linked_list_001_node_t *head, int32_t key);
int pat_ds_linked_list_001_insert_after(pat_ds_linked_list_001_node_t *position, pat_ds_linked_list_001_node_t *node);
pat_ds_linked_list_001_node_t * pat_ds_linked_list_001_remove_first(pat_ds_linked_list_001_node_t **head, int32_t key);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Follow next pointers for search.
2. Splice node after position.
3. Remove through pointer-to-link so head removal is uniform.

## Worked trace

1->2->3, remove 2 -> 1->3; removed node next=NULL.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_ds_linked_list_001 | pat_ds_linked_list_001_node_t *head | R0 |
| pat_ds_linked_list_001 | int32_t key | R1 |
| pat_ds_linked_list_001_insert_after | pat_ds_linked_list_001_node_t *position | R0 |
| pat_ds_linked_list_001_insert_after | pat_ds_linked_list_001_node_t *node | R1 |
| pat_ds_linked_list_001_remove_first | pat_ds_linked_list_001_node_t **head | R0 |
| pat_ds_linked_list_001_remove_first | int32_t key | R1 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(n) search/removal, O(1) insertion and internal space.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  pat_ds_linked_list_001_node_t b = {2, NULL}, a = {1, &b};
  return pat_ds_linked_list_001(&a, 2) == &b && pat_ds_linked_list_001(&a, 3) == NULL;
}
static int pattern_edge_vectors(void) {
  pat_ds_linked_list_001_node_t lone = {1, NULL};
  if (pat_ds_linked_list_001_insert_after(&lone, &lone) || lone.next != NULL)
    return 0;
  pat_ds_linked_list_001_node_t c = {3, NULL}, b = {2, NULL}, a = {1, &b};
  pat_ds_linked_list_001_node_t *head = &a;
  return pat_ds_linked_list_001_insert_after(&a, &c) && a.next == &c &&
         pat_ds_linked_list_001_remove_first(&head, 3) == &c && c.next == NULL &&
         pat_ds_linked_list_001_remove_first(&head, 9) == NULL;
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

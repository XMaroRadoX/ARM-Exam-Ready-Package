# PAT-DS-LINKED-LIST-001: Singly linked-list operations

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: traverse search insert remove nodes.

## C contract and variants

Primary export: `pat_ds_linked_list_001_node_t * pat_ds_linked_list_001(pat_ds_linked_list_001_node_t *head, int32_t key);`

All public reference variants:

```c
pat_ds_linked_list_001_node_t * pat_ds_linked_list_001(pat_ds_linked_list_001_node_t *head, int32_t key);
int pat_ds_linked_list_001_insert_after(pat_ds_linked_list_001_node_t *position, pat_ds_linked_list_001_node_t *node);
pat_ds_linked_list_001_node_t * pat_ds_linked_list_001_remove_first(pat_ds_linked_list_001_node_t **head, int32_t key);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Follow next pointers for search.
2. Splice node after position.
3. Remove through pointer-to-link so head removal is uniform.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-DS-LINKED-LIST-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-DS-LINKED-LIST-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `head` — `pat_ds_linked_list_001_node_t *head` |
| `R1` | `key` — `int32_t key` |

`R0` carries `pat_ds_linked_list_001_node_t *`.

Classification: **leaf**. Saved-register bytes: **0**. Local bytes: **0**. Static frame total: **0 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(n) search/removal, O(1) insertion and internal space.

## Boundary and adaptation checklist

- Current boundary policy: empty, one-element, duplicate, invalid-pointer/capacity and arithmetic-limit behavior is executable in the vector suite below.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: empty, one-element, duplicate, invalid-pointer/capacity and arithmetic-limit behavior is executable in the vector suite below. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

```c
static int pattern_core_vector(void) {
  pat_ds_linked_list_001_node_t b = {2, NULL}, a = {1, &b};
  return pat_ds_linked_list_001(&a, 2) == &b &&
         pat_ds_linked_list_001(&a, 3) == NULL;
}
static int pattern_edge_vectors(void) {
  pat_ds_linked_list_001_node_t c = {3, NULL}, b = {2, NULL}, a = {1, &b};
  pat_ds_linked_list_001_node_t *head = &a;
  return pat_ds_linked_list_001_insert_after(&a, &c) && a.next == &c &&
         pat_ds_linked_list_001_remove_first(&head, 3) == &c &&
         c.next == NULL &&
         pat_ds_linked_list_001_remove_first(&head, 9) == NULL;
}
```

## Historical grounding

No historical occurrence is claimed; this entry is supplementary preparation.

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `COMPILE_ONLY`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

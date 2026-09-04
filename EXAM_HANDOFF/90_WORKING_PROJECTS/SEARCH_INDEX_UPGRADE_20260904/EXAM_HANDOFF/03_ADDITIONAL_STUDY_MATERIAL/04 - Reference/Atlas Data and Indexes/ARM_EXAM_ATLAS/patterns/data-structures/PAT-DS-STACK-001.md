# PAT-DS-STACK-001: Array-backed stack

Priority: **supplementary reference**.

## Recognition phrases

Likely wording: bounded LIFO push pop.

## C contract and variants

Primary export: `int pat_ds_stack_001(int32_t *a, uint32_t cap, uint32_t *top, int push, int32_t *value);`

All public reference variants:

```c
int pat_ds_stack_001(int32_t *a, uint32_t cap, uint32_t *top, int push, int32_t *value);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Reject invalid/full/empty state.
2. Push at top then increment.
3. Pop by decrement then load.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-DS-STACK-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-DS-STACK-001/arm/implementation.s)
- ARM style: Compiler-derived matching ARMASM; use it for instruction comparison, not as a memorization template.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `a` — `int32_t *a` |
| `R1` | `cap` — `uint32_t cap` |
| `R2` | `top` — `uint32_t *top` |
| `R3` | `push` — `int push` |
| `caller [SP, #0]` | `value` — `int32_t *value` |

`R0` carries `int`.

Classification: **leaf**. Saved-register bytes: **8**. Local bytes: **0**. Static frame total: **8 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(1) per operation, O(capacity) caller storage.

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
  int32_t a[2], v = 7, o = 0;
  uint32_t top = 0;
  return pat_ds_stack_001(a, 2, &top, 1, &v) &&
         pat_ds_stack_001(a, 2, &top, 0, &o) && o == 7;
}
static int pattern_edge_vectors(void) {
  int32_t a[1], v = 1, o = 0;
  uint32_t top = 0;
  return !pat_ds_stack_001(a, 1, &top, 0, &o) &&
         pat_ds_stack_001(a, 1, &top, 1, &v) &&
         !pat_ds_stack_001(a, 1, &top, 1, &v) &&
         pat_ds_stack_001(a, 1, &top, 0, &o) && o == 1;
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

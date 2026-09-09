# PAT-ALG-INDIRECT-RECURRENCE-001: Indirect-index recurrence

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: Recaman or Hofstadter recurrence indexes earlier terms.

## C contract and variants

Primary export: `uint32_t pat_alg_indirect_recurrence_001(uint32_t *output, uint32_t count);`

All public reference variants:

```c
uint32_t pat_alg_indirect_recurrence_001(uint32_t *output, uint32_t count);
uint32_t pat_alg_indirect_recurrence_001_hofstadter_q(uint32_t *output, uint32_t count);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Seed sequence.
2. Propose previous-index subtraction.
3. Scan earlier terms for duplicates.
4. Otherwise add index.
5. Store term.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-INDIRECT-RECURRENCE-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-INDIRECT-RECURRENCE-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `output` — `uint32_t *output` |
| `R1` | `count` — `uint32_t count` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **32**. Local bytes: **0**. Static frame total: **32 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(n^2) time for duplicate scans, O(n) output space; Hofstadter Q is O(n).

## Boundary and adaptation checklist

- Current boundary policy: null/empty returns zero; one element is the seed; earlier terms are scanned before subtraction is accepted.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: null/empty returns zero; one element is the seed; earlier terms are scanned before subtraction is accepted. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

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
```

## Historical grounding

- [E2026-02-03-A3-Q1](../../exams/2026/2026-02-03-A3/Q1_ASSEMBLY.md)
- [E2026-02-18-A1-Q1](../../exams/2026/2026-02-18-A1/Q1_ASSEMBLY.md)
- [E2026-02-18-A2-Q1](../../exams/2026/2026-02-18-A2/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

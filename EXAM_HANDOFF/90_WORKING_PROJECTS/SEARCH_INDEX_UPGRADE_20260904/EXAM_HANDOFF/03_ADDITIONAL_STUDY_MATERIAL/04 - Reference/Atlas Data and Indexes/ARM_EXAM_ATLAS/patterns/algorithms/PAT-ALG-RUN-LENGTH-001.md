# PAT-ALG-RUN-LENGTH-001: Run-length encoding

Priority: **high priority — directly exam-derived**.

## Recognition phrases

Likely wording: compress consecutive equal values including final run.

## C contract and variants

Primary export: `uint32_t pat_alg_run_length_001(const uint8_t *in, uint32_t n, uint8_t *value, uint8_t *run, uint32_t cap);`

All public reference variants:

```c
uint32_t pat_alg_run_length_001(const uint8_t *in, uint32_t n, uint8_t *value, uint8_t *run, uint32_t cap);
```

Fixed-width types state element width and signedness. Pointer arguments name the first object; counts and capacities are separate values. Mutation occurs only through non-const output pointers.

## Pseudocode

1. Start at first unconsumed byte.
2. Count equal bytes up to 255.
3. Verify output capacity.
4. Emit value/count.
5. Repeat including final run.

## Source pair

- [Readable C](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-RUN-LENGTH-001/c/reference.c)
- [ARMASM implementation](../../../../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/PAT-ALG-RUN-LENGTH-001/arm/implementation.s)
- ARM style: Handwritten exam-style ARMASM with named loops and an explicit frame.

## AAPCS register plan

| Entry location | Meaning |
|---|---|
| `R0` | `in` — `const uint8_t *in` |
| `R1` | `n` — `uint32_t n` |
| `R2` | `value` — `uint8_t *value` |
| `R3` | `run` — `uint8_t *run` |
| `caller [SP, #0]` | `cap` — `uint32_t cap` |

`R0` carries `uint32_t`.

Classification: **leaf**. Saved-register bytes: **32**. Local bytes: **0**. Static frame total: **32 bytes**.

No `BL` instruction occurs. The routine still restores every modified R4-R11 register and returns with its original SP.

## Complexity

O(n) time, O(1) internal space plus output.

## Boundary and adaptation checklist

- Current boundary policy: empty input returns zero runs; a run is split at 255; insufficient capacity returns zero.
- Change element load/store width together with the C type.
- Change signed/unsigned branch conditions together with the comparison contract.
- Recalculate caller stack offsets after any prologue change.
- Keep caller-provided capacity and maximum-depth assumptions explicit.

### Structured edge-case matrix

| Case | Required check and current evidence |
|---|---|
| Empty or zero-size | Apply this pattern's current policy: empty input returns zero runs; a run is split at 255; insufficient capacity returns zero. The exact zero-size assertion is in `pattern_edge_vectors()` when meaningful. |
| One element / smallest valid object | Must take the direct base path without reading a neighbor or second element; the edge vector exercises the smallest meaningful input. |
| Duplicates / repeated values | Preserve stability, consume once, count all, or ignore repeats exactly as the named variant promises; duplicate assertions are included where the algorithm can observe duplicates. |
| Maximum size / capacity | Validate capacity before each write and keep caller scratch, queue, stack, table, or depth bounds explicit. No test label implies unlimited storage. |
| Signed limit / overflow | Use the fixed-width contract, widened intermediates, checked multiplication/addition, saturation, or documented wraparound. Never infer signed overflow behavior. |
| Invalid pointer / index / dimension | Return the documented failure value before dereferencing. Inputs that cannot be invalid by prototype are marked by omission in the exact vector code. |

## Deterministic host vectors

The following compiled test functions contain the core result plus relevant empty, one-element, duplicate, invalid, limit or overflow cases. A zero process exit means both functions passed.

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
```

## Historical grounding

- [E2026-02-03-A2-Q1](../../exams/2026/2026-02-03-A2/Q1_ASSEMBLY.md)

## Verification boundary

- C: `HOST_EDGE_TESTED_C` after strict-warning compilation and both deterministic vector functions pass.
- ARM: `SIMULATOR_EXECUTED_PASS`. `SIMULATOR_EXECUTED_PASS` is used only when the harness report records output, callee-saved-register, SP-restoration and guard checks.
- Physical board: `PHYSICAL_BOARD_NOT_TESTED` unless a separate board report exists.

## Related reading

- [Defining data in C and ARMASM](../../../../../01%20-%20Learn/01%20-%20C%20Foundations/defining-data.md)

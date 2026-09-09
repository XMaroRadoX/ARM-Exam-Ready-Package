# PAT-ALG-STRING-PRIMITIVES-001: Bounded string primitives

## Recognition phrases

Bounded length and unsigned-byte comparison; NUL-terminated source strings. Copy truncates to capacity-1 and always terminates when capacity>0; it does not report truncation as failure. Substring search returns first index or -1.

## C contract and variants

```c
uint32_t pat_alg_string_primitives_001_length(const char *text, uint32_t limit);
int32_t pat_alg_string_primitives_001_compare(const char *first, const char *second, uint32_t limit);
uint32_t pat_alg_string_primitives_001_copy(char *destination, uint32_t capacity, const char *source);
int32_t pat_alg_string_primitives_001(const char *text, const char *needle, uint32_t limit);
```

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

1. Scan with explicit limit for length.
2. Compare unsigned bytes.
3. Bounded-copy with terminator.
4. Test each possible substring start.

## Worked trace

Copy "abcd" into capacity 4 -> "abc" plus terminator, return 3.

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.

## AAPCS register plan

| Function | Parameter | Entry location |
|---|---|---|
| pat_alg_string_primitives_001_length | const char *text | R0 |
| pat_alg_string_primitives_001_length | uint32_t limit | R1 |
| pat_alg_string_primitives_001_compare | const char *first | R0 |
| pat_alg_string_primitives_001_compare | const char *second | R1 |
| pat_alg_string_primitives_001_compare | uint32_t limit | R2 |
| pat_alg_string_primitives_001_copy | char *destination | R0 |
| pat_alg_string_primitives_001_copy | uint32_t capacity | R1 |
| pat_alg_string_primitives_001_copy | const char *source | R2 |
| pat_alg_string_primitives_001 | const char *text | R0 |
| pat_alg_string_primitives_001 | const char *needle | R1 |
| pat_alg_string_primitives_001 | uint32_t limit | R2 |


Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

O(limit) for length/compare/copy and O(limit*needle length) for naive search.

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

```c
static int pattern_core_vector(void) {
  return pat_alg_string_primitives_001("abcabc", "cab", 6) == 2 &&
         pat_alg_string_primitives_001("abc", "z", 3) == -1;
}
static int pattern_edge_vectors(void) {
  char out[4];
  return pat_alg_string_primitives_001_length("abc", 2) == 2 &&
         pat_alg_string_primitives_001_compare("a", "b", 2) < 0 &&
         pat_alg_string_primitives_001_copy(out, 4, "abcd") == 3 && out[3] == '\0' &&
         pat_alg_string_primitives_001("", "", 1) == 0 &&
         pat_alg_string_primitives_001(NULL, "a", 1) == -1;
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

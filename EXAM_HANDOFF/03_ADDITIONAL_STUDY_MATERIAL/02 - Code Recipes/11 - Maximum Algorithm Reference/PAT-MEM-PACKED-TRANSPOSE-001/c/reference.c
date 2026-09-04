#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Packed 8x8 bit-matrix transpose.
 * Recognition cue: transpose packed binary matrix rows and columns.
 *
 * Contract rules:
 * - Fixed-width types make width and signedness part of the interface.
 * - A pointer never carries its length; count/capacity arguments are explicit.
 * - const input objects are not mutated. Non-const outputs may be changed only
 *   within their documented bounds.
 * - Invalid, empty, duplicate and arithmetic-limit behavior is executable in
 *   pattern_edge_vectors() and described in the adjacent README.
 *
 * Trace the validation step first, then the main loop/recurrence invariant,
 * then the final result or capacity check. Public suffix functions are named
 * variants of the same advertised pattern, not unrelated shortcuts.
 */

/* Primary algorithm and its named variants. */
uint64_t pat_mem_packed_transpose_001(uint64_t x) {
  uint64_t y = 0;
  uint32_t r, c;
  for (r = 0; r < 8; r++)
    for (c = 0; c < 8; c++)
      y |= ((x >> (r * 8u + c)) & 1u) << (c * 8u + r);
  return y;
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  return pat_mem_packed_transpose_001(UINT64_C(1) << 10) == (UINT64_C(1) << 17);
}
static int pattern_edge_vectors(void) {
  uint64_t x = UINT64_C(0x0123456789abcdef);
  return pat_mem_packed_transpose_001(0) == 0 &&
         pat_mem_packed_transpose_001(pat_mem_packed_transpose_001(x)) == x;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int main(void) { return pattern_test_suite(); }
#endif

#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Packed binary matrix multiplication.
 * Recognition cue: multiply packed binary matrices over GF(2).
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
uint64_t pat_alg_packed_matmul_001(uint64_t a, uint64_t b) {
  uint64_t o = 0;
  uint32_t r, c, k;
  for (r = 0; r < 8; r++)
    for (c = 0; c < 8; c++) {
      uint32_t v = 0;
      for (k = 0; k < 8; k++)
        v ^= (uint32_t)((a >> (r * 8 + k)) & (b >> (k * 8 + c)) & 1u);
      o |= (uint64_t)v << (r * 8 + c);
    }
  return o;
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  uint64_t i = UINT64_C(0x8040201008040201);
  return pat_alg_packed_matmul_001(i, i) == i;
}
static int pattern_edge_vectors(void) {
  uint64_t identity = UINT64_C(0x8040201008040201);
  return pat_alg_packed_matmul_001(0, identity) == 0 &&
         pat_alg_packed_matmul_001(identity, 0) == 0;
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

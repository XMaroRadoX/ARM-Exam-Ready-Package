#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Integer square root.
 * Recognition cue: floor square root without floating point.
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
uint32_t pat_alg_integer_sqrt_001(uint32_t n) {
  uint32_t bit = 1u << 30, res = 0;
  while (bit > n)
    bit >>= 2;
  while (bit) {
    if (n >= res + bit) {
      n -= res + bit;
      res = (res >> 1) + bit;
    } else
      res >>= 1;
    bit >>= 2;
  }
  return res;
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  return pat_alg_integer_sqrt_001(0) == 0 &&
         pat_alg_integer_sqrt_001(15) == 3 && pat_alg_integer_sqrt_001(16) == 4;
}
static int pattern_edge_vectors(void) {
  return pat_alg_integer_sqrt_001(1) == 1 &&
         pat_alg_integer_sqrt_001(UINT32_MAX) == 65535u;
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

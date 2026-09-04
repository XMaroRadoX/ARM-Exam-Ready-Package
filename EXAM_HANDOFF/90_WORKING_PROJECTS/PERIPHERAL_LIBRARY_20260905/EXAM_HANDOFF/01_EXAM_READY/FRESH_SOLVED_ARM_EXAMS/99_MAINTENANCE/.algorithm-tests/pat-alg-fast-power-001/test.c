#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Exponentiation by squaring.
 * Recognition cue: fast power modular exponentiation.
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

uint32_t pat_alg_fast_power_001(uint32_t base, uint32_t exponent,
                                uint32_t modulus);

int pat_alg_fast_power_001_checked(uint32_t base, uint32_t exponent,
                                   uint32_t *result);



static int pattern_core_vector(void) {
  return pat_alg_fast_power_001(3, 4, 5) == 1;
}
static int pattern_edge_vectors(void) {
  uint32_t out = 0;
  return pat_alg_fast_power_001(7, 0, 5) == 1 &&
         pat_alg_fast_power_001_checked(3, 4, &out) && out == 81 &&
         !pat_alg_fast_power_001_checked(UINT32_MAX, 2, &out);
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

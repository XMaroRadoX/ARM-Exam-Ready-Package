#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Clamp absolute saturation and overflow.
 * Recognition cue: clamp signed arithmetic without overflow.
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

int32_t pat_alg_saturating_arithmetic_001(int64_t value, int32_t minimum,
                                          int32_t maximum) {
  if (minimum > maximum) {
    return minimum;
  }
  if (value < minimum) {
    return minimum;
  }
  if (value > maximum) {
    return maximum;
  }
  return (int32_t)value;
}

uint32_t pat_alg_saturating_arithmetic_001_abs_i32(int32_t value) {
  return (value < 0) ? (uint32_t)(-(int64_t)value) : (uint32_t)value;
}

int32_t pat_alg_saturating_arithmetic_001_add_i32(int32_t first,
                                                  int32_t second) {
  return pat_alg_saturating_arithmetic_001((int64_t)first + second, INT32_MIN,
                                           INT32_MAX);
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  return pat_alg_saturating_arithmetic_001(50, 0, 10) == 10 &&
         pat_alg_saturating_arithmetic_001(-2, 0, 10) == 0;
}
static int pattern_edge_vectors(void) {
  return pat_alg_saturating_arithmetic_001(5, 10, 0) == 10 &&
         pat_alg_saturating_arithmetic_001_abs_i32(INT32_MIN) ==
             UINT32_C(2147483648) &&
         pat_alg_saturating_arithmetic_001_add_i32(INT32_MAX, 1) == INT32_MAX &&
         pat_alg_saturating_arithmetic_001_add_i32(INT32_MIN, -1) == INT32_MIN;
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

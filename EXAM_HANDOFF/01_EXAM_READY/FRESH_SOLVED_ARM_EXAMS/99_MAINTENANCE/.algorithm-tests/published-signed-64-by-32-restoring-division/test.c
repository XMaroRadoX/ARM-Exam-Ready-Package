#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Signed 64-by-32 restoring division.
 * Recognition cue: divide signed 64-bit dividend by signed 32-bit divisor.
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
int64_t algorithm_signed_64_by_32_restoring_division(int64_t dividend, int32_t divisor,
                                                     int32_t *remainder);

static int pattern_core_vector(void) {
  int32_t r = 0;
  return algorithm_signed_64_by_32_restoring_division(-15, 2, &r) == -7 && r == -1;
}
static int pattern_edge_vectors(void) {
  int32_t rem_limit = 99;
  if (algorithm_signed_64_by_32_restoring_division(INT64_MIN, 1, &rem_limit) !=
          INT64_MIN ||
      rem_limit != 0 ||
      algorithm_signed_64_by_32_restoring_division(INT64_MIN, -1, &rem_limit) !=
          INT64_MIN)
    return 0;
  int32_t r = 7;
  return algorithm_signed_64_by_32_restoring_division(0, 5, &r) == 0 && r == 0 &&
         algorithm_signed_64_by_32_restoring_division(15, -2, &r) == -7 && r == 1 &&
         algorithm_signed_64_by_32_restoring_division(9, 0, &r) == 0 && r == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

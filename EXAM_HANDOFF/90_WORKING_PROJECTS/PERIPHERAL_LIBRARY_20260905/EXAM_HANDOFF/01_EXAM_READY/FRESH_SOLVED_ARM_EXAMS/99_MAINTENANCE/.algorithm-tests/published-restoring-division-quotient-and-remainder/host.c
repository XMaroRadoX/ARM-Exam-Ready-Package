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
int64_t algorithm_restoring_division_quotient_and_remainder(int64_t dividend,
                                                            int32_t divisor,
                                                            int32_t *remainder) {
  uint64_t q = 0, r = 0, u;
  uint32_t d;
  int negq, negr;
  int i;
  if (!divisor) {
    if (remainder)
      *remainder = 0;
    return 0;
  }
  negq = ((dividend < 0) ^ (divisor < 0));
  negr = (dividend < 0);
  u = (dividend < 0) ? (uint64_t)(-(dividend + 1)) + 1u : (uint64_t)dividend;
  d = (divisor < 0) ? (uint32_t)(-(int64_t)divisor) : (uint32_t)divisor;
  for (i = 63; i >= 0; i--) {
    r = (r << 1) | ((u >> (uint32_t)i) & 1u);
    if (r >= d) {
      r -= d;
      q |= UINT64_C(1) << (uint32_t)i;
    }
  }
  if (remainder) {
    *remainder = negr ? -(int32_t)r : (int32_t)r;
  }
  if (q == (UINT64_C(1) << 63))
    return INT64_MIN;
  if (q == (UINT64_C(1) << 63))
    return INT64_MIN;
  return negq ? -(int64_t)q : (int64_t)q;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


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
int64_t algorithm_restoring_division_quotient_and_remainder(int64_t dividend,
                                                            int32_t divisor,
                                                            int32_t *remainder);

static int pattern_core_vector(void) {
  int32_t r = 0;
  return algorithm_restoring_division_quotient_and_remainder(-15, 2, &r) == -7 &&
         r == -1;
}
static int pattern_edge_vectors(void) {
  int32_t rem_limit = 99;
  if (algorithm_restoring_division_quotient_and_remainder(INT64_MIN, 1, &rem_limit) !=
          INT64_MIN ||
      rem_limit != 0 ||
      algorithm_restoring_division_quotient_and_remainder(INT64_MIN, -1, &rem_limit) !=
          INT64_MIN)
    return 0;
  int32_t r = 7;
  return algorithm_restoring_division_quotient_and_remainder(0, 5, &r) == 0 && r == 0 &&
         algorithm_restoring_division_quotient_and_remainder(15, -2, &r) == -7 &&
         r == 1 && algorithm_restoring_division_quotient_and_remainder(9, 0, &r) == 0 &&
         r == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

int main(void){return test_main();}

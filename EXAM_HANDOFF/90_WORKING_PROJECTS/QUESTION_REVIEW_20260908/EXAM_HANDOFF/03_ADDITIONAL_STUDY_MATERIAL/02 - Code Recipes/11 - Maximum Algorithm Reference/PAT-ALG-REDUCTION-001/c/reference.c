#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Signed min max and sum reduction.
 * Recognition cue: reduce array to minimum maximum and sum.
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

typedef struct {
  int32_t minimum;
  int32_t maximum;
  int64_t sum;
} pat_alg_reduction_001_signed_result_t;

typedef struct {
  uint32_t minimum;
  uint32_t maximum;
  uint64_t sum;
} pat_alg_reduction_001_unsigned_result_t;

int pat_alg_reduction_001(const int32_t *values, uint32_t count,
                          pat_alg_reduction_001_signed_result_t *result) {
  uint32_t index;

  if ((values == NULL) || (result == NULL) || (count == 0u)) {
    return 0;
  }
  result->minimum = values[0];
  result->maximum = values[0];
  result->sum = 0;
  for (index = 0u; index < count; ++index) {
    if (values[index] < result->minimum) {
      result->minimum = values[index];
    }
    if (values[index] > result->maximum) {
      result->maximum = values[index];
    }
    result->sum += values[index];
  }
  return 1;
}

int pat_alg_reduction_001_unsigned(
    const uint32_t *values, uint32_t count,
    pat_alg_reduction_001_unsigned_result_t *result) {
  uint32_t index;

  if ((values == NULL) || (result == NULL) || (count == 0u)) {
    return 0;
  }
  result->minimum = values[0];
  result->maximum = values[0];
  result->sum = 0u;
  for (index = 0u; index < count; ++index) {
    if (values[index] < result->minimum) {
      result->minimum = values[index];
    }
    if (values[index] > result->maximum) {
      result->maximum = values[index];
    }
    result->sum += values[index];
  }
  return 1;
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  int32_t a[] = {-2, 5, 1};
  pat_alg_reduction_001_signed_result_t r;
  return pat_alg_reduction_001(a, 3, &r) && r.minimum == -2 && r.maximum == 5 &&
         r.sum == 4;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {INT32_MIN, INT32_MAX};
  uint32_t u[] = {0, UINT32_MAX};
  pat_alg_reduction_001_signed_result_t s;
  pat_alg_reduction_001_unsigned_result_t r;
  return !pat_alg_reduction_001(NULL, 0, &s) &&
         pat_alg_reduction_001(a, 2, &s) && s.sum == -1 &&
         pat_alg_reduction_001_unsigned(u, 2, &r) && r.sum == UINT32_MAX;
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

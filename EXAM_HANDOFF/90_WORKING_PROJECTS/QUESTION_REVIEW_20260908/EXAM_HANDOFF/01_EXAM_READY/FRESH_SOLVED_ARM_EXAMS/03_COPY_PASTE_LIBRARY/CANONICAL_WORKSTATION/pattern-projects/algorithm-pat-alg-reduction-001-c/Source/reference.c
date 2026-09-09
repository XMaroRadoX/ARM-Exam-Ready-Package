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
} algorithm_algorithm_pat_alg_reduction_001_c_signed_result_t;

typedef struct {
  uint32_t minimum;
  uint32_t maximum;
  uint64_t sum;
} algorithm_algorithm_pat_alg_reduction_001_c_unsigned_result_t;

int algorithm_algorithm_pat_alg_reduction_001_c(const int32_t *values, uint32_t count,
                          algorithm_algorithm_pat_alg_reduction_001_c_signed_result_t *result) {
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

int algorithm_algorithm_pat_alg_reduction_001_c_unsigned(
    const uint32_t *values, uint32_t count,
    algorithm_algorithm_pat_alg_reduction_001_c_unsigned_result_t *result) {
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


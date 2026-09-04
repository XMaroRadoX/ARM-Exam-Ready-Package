#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Prefix sums and range sums.
 * Recognition cue: precompute cumulative sums answer ranges.
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

int algorithm_constant_time_range_sums(const int32_t *values, uint32_t count,
                                       int64_t *prefix) {
  uint32_t index;

  if ((prefix == NULL) || ((values == NULL) && (count != 0u)) ||
      count >= UINT32_MAX / 8u) {
    return 0;
  }
  prefix[0] = 0;
  for (index = 0u; index < count; ++index) {
    prefix[index + 1u] = prefix[index] + values[index];
  }
  return 1;
}

int algorithm_constant_time_range_sums_range(const int64_t *prefix, uint32_t count,
                                             uint32_t begin, uint32_t end,
                                             int64_t *sum) {
  if ((prefix == NULL) || (sum == NULL) || (begin > end) || (end > count)) {
    return 0;
  }
  *sum = prefix[end] - prefix[begin];
  return 1;
}

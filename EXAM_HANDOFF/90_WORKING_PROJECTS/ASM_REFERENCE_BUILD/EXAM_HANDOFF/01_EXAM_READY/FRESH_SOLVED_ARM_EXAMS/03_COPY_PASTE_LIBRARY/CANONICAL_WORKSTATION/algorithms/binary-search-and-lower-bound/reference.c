#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Binary search and lower bound.
 * Recognition cue: sorted array binary search insertion position.
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

uint32_t algorithm_binary_search_and_lower_bound(const int32_t *values, uint32_t count,
                                                 int32_t key) {
  uint32_t low = 0u;
  uint32_t high = count;

  if (values == NULL) {
    return 0u;
  }
  while (low < high) {
    uint32_t middle = low + (high - low) / 2u;
    if (values[middle] < key) {
      low = middle + 1u;
    } else {
      high = middle;
    }
  }
  return low;
}

int32_t algorithm_binary_search_and_lower_bound_exact(const int32_t *values,
                                                      uint32_t count, int32_t key) {
  uint32_t position = algorithm_binary_search_and_lower_bound(values, count, key);
  if ((values != NULL) && (position < count) && (values[position] == key)) {
    return (int32_t)position;
  }
  return -1;
}

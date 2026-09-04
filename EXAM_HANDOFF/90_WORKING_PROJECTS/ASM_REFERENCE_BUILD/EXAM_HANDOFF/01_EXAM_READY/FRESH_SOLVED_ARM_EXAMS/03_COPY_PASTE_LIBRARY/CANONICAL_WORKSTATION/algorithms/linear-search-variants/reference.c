#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Linear search variants.
 * Recognition cue: find first last or all matches.
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

int32_t algorithm_linear_search_variants(const int32_t *values, uint32_t count,
                                         int32_t key) {
  uint32_t index;

  if (values == NULL) {
    return -1;
  }
  for (index = 0u; index < count; ++index) {
    if (values[index] == key) {
      return (int32_t)index;
    }
  }
  return -1;
}

int32_t algorithm_linear_search_variants_last(const int32_t *values, uint32_t count,
                                              int32_t key) {
  while ((values != NULL) && (count != 0u)) {
    --count;
    if (values[count] == key) {
      return (int32_t)count;
    }
  }
  return -1;
}

uint32_t algorithm_linear_search_variants_all(const int32_t *values, uint32_t count,
                                              int32_t key, uint32_t *indexes,
                                              uint32_t capacity) {
  uint32_t index;
  uint32_t matches = 0u;

  if ((values == NULL) || ((indexes == NULL) && (capacity != 0u))) {
    return 0u;
  }
  for (index = 0u; index < count; ++index) {
    if (values[index] == key) {
      if (matches < capacity) {
        indexes[matches] = index;
      }
      ++matches;
    }
  }
  return matches;
}

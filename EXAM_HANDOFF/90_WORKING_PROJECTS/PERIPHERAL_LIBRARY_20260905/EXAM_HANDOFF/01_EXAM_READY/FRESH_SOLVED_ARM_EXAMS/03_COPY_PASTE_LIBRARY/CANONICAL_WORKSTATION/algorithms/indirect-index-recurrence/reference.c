#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Indirect-index recurrence.
 * Recognition cue: Recaman or Hofstadter recurrence indexes earlier terms.
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

uint32_t algorithm_indirect_index_recurrence(uint32_t *output, uint32_t count) {
  uint32_t index;

  if ((output == NULL) || (count == 0u)) {
    return 0u;
  }
  output[0] = 0u;
  for (index = 1u; index < count; ++index) {
    uint32_t previous = output[index - 1u];
    uint32_t candidate = previous + index;
    uint32_t scan;
    int candidate_used = 0;

    if (previous >= index) {
      candidate = previous - index;
      for (scan = 0u; scan < index; ++scan) {
        if (output[scan] == candidate) {
          candidate_used = 1;
          break;
        }
      }
    }
    if ((previous >= index) && !candidate_used)
      output[index] = candidate;
    else {
      if (previous > UINT32_MAX - index)
        return 0;
      output[index] = previous + index;
    }
  }
  return count;
}

uint32_t algorithm_indirect_index_recurrence_hofstadter_q(uint32_t *output,
                                                          uint32_t count) {
  if (!output || !count)
    return 0;
  output[0] = 1;
  if (count == 1)
    return 1;
  output[1] = 1;
  for (uint32_t i = 2; i < count; i++) {
    uint32_t a = output[i - 1], b = output[i - 2];
    if (!a || !b || a > i || b > i)
      return 0;
    a = output[i - a];
    b = output[i - b];
    if (a > UINT32_MAX - b)
      return 0;
    output[i] = a + b;
  }
  return count;
}

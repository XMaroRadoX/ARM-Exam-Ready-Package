#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Left and right array rotation.
 * Recognition cue: rotate array using reversal.
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

static void pat_alg_array_rotation_001_reverse_range(int32_t *values,
                                                     uint32_t left,
                                                     uint32_t right) {
  while (left < right) {
    int32_t temporary = values[left];
    values[left] = values[right];
    values[right] = temporary;
    ++left;
    --right;
  }
}

void pat_alg_array_rotation_001(int32_t *values, uint32_t count,
                                uint32_t positions) {
  if ((values == NULL) || (count < 2u)) {
    return;
  }
  positions %= count;
  if (positions == 0u) {
    return;
  }
  pat_alg_array_rotation_001_reverse_range(values, 0u, positions - 1u);
  pat_alg_array_rotation_001_reverse_range(values, positions, count - 1u);
  pat_alg_array_rotation_001_reverse_range(values, 0u, count - 1u);
}

void pat_alg_array_rotation_001_right(int32_t *values, uint32_t count,
                                      uint32_t positions) {
  if (count != 0u) {
    pat_alg_array_rotation_001(values, count, count - (positions % count));
  }
}

int pat_alg_array_rotation_001_with_scratch(int32_t *values, uint32_t count,
                                            uint32_t positions,
                                            int32_t *scratch,
                                            uint32_t scratch_count) {
  uint32_t index;

  if ((values == NULL) || (scratch == NULL) || (scratch_count < count) || values == scratch) {
    return 0;
  }
  if (count == 0u) {
    return 1;
  }
  positions %= count;
  for (index = 0u; index < count; ++index) {
    scratch[index] = values[index >= count-positions ? index-(count-positions) : index+positions];
  }
  for (index = 0u; index < count; ++index) {
    values[index] = scratch[index];
  }
  return 1;
}


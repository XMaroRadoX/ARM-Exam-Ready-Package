#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Concatenate two arrays within capacity
 * Contract: Write left followed by right. Reject count overflow, insufficient capacity,
 * or invalid nonempty pointers before writing. The output must not overlap either
 * input. Empty inputs are allowed. Method:
 * 1. Validate the total count and pointers.
 * 2. Copy the left array.
 * 3. Continue with the right array.
 */
int array_concatenate(const int32_t *left, uint32_t left_count, const int32_t *right,
                      uint32_t right_count, int32_t *output, uint32_t capacity) {
  if (left_count > UINT32_MAX - right_count)
    return 0;
  uint32_t total = left_count + right_count;
  if (capacity < total || (!left && left_count) || (!right && right_count) ||
      (!output && total))
    return 0;
  for (uint32_t i = 0; i < left_count; ++i)
    output[i] = left[i];
  for (uint32_t i = 0; i < right_count; ++i)
    output[left_count + i] = right[i];
  return 1;
}

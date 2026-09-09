#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Compare bounded strings for equality
 * Contract: Return 1 for equal strings, 0 for unequal strings, and -1 when either input
 * is null or lacks NUL within its capacity. Both strings are fully validated before
 * comparison. Method:
 * 1. Find both bounded lengths.
 * 2. Reject unequal lengths.
 * 3. Compare exactly the characters before NUL.
 */
static int string_length_for_equal(const uint8_t *text, uint32_t capacity,
                                   uint32_t *length) {
  if (!text || !length)
    return 0;
  for (uint32_t i = 0; i < capacity; ++i)
    if (text[i] == 0) {
      *length = i;
      return 1;
    }
  return 0;
}
int32_t strings_equal_bounded(const uint8_t *left, uint32_t left_capacity,
                              const uint8_t *right, uint32_t right_capacity) {
  uint32_t left_length, right_length;
  if (!string_length_for_equal(left, left_capacity, &left_length) ||
      !string_length_for_equal(right, right_capacity, &right_length))
    return -1;
  if (left_length != right_length)
    return 0;
  for (uint32_t i = 0; i < left_length; ++i)
    if (left[i] != right[i])
      return 0;
  return 1;
}

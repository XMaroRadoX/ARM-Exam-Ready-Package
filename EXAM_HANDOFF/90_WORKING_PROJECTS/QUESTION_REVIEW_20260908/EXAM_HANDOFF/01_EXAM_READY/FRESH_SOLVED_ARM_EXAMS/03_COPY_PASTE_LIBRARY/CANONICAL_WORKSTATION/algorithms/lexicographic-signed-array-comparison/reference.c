#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Lexicographically compare two signed arrays
 * Contract: Return -1, 0, or 1 using signed element order, then shorter-prefix order. A
 * null pointer is valid only with a zero count; invalid input returns 2. Method:
 * 1. Compare corresponding values up to the shorter count.
 * 2. Return at the first unequal signed pair.
 * 3. If the common prefix matches, compare lengths.
 */
int32_t arrays_compare_lexicographic(const int32_t *left, uint32_t left_count,
                                     const int32_t *right, uint32_t right_count) {
  if ((!left && left_count) || (!right && right_count))
    return 2;
  uint32_t n = left_count < right_count ? left_count : right_count;
  for (uint32_t i = 0; i < n; ++i) {
    if (left[i] < right[i])
      return -1;
    if (left[i] > right[i])
      return 1;
  }
  return left_count < right_count ? -1 : left_count > right_count ? 1 : 0;
}

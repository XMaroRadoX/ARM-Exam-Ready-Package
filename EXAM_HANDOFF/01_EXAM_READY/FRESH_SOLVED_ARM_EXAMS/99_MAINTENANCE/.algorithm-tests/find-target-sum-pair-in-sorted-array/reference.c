#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Find a target-sum pair in a sorted array
 * Contract: Input must be ascending. Find two distinct indexes whose exact 64-bit sum equals target. Output pointers must be valid and distinct; failure writes nothing.
 * Method:
 * 1. Start at both ends.
 * 2. Compare the widened sum with target.
 * 3. Move the left or right index until a pair is found.
 */
int array_pair_sum_sorted(const int32_t *values, uint32_t count,
                    int32_t target, uint32_t *first_out,
                    uint32_t *second_out) {
  if (!values || !first_out || !second_out || first_out == second_out) return 0;
  uint32_t first = 0, second = count - 1;
  while (first < second) {
    int64_t sum = (int64_t)values[first] + values[second];
    if (sum == target) { *first_out = first; *second_out = second; return 1; }
    if (sum < target) ++first; else --second;
  }
  return 0;
}

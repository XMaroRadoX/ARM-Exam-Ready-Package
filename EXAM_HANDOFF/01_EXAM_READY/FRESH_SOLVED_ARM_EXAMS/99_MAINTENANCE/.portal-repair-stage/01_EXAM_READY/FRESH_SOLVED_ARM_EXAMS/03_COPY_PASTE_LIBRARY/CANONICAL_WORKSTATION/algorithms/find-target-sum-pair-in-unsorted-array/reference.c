#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Find a target-sum pair in a unsorted array
 * Contract: Find two distinct indexes whose exact 64-bit sum equals target. Output
 * pointers must be valid and distinct; failure writes nothing. Method:
 * 1. Enumerate first indexes from low to high.
 * 2. Enumerate each later second index.
 * 3. Return the lexicographically first matching pair.
 */
int array_pair_sum_unsorted(const int32_t *values, uint32_t count, int32_t target,
                            uint32_t *first_out, uint32_t *second_out) {
  if (!values || !first_out || !second_out || first_out == second_out)
    return 0;
  for (uint32_t first = 0; first < count; ++first)
    for (uint32_t second = first + 1; second < count; ++second)
      if ((int64_t)values[first] + values[second] == target) {
        *first_out = first;
        *second_out = second;
        return 1;
      }
  return 0;
}

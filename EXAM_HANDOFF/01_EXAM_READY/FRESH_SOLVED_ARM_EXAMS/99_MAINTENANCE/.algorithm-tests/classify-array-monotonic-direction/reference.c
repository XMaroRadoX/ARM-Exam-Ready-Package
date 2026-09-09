#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Classify an array monotonic direction
 * Contract: Return 1 for nondecreasing, -1 for nonincreasing, 0 for constant or fewer than two elements, and 2 for non-monotonic or invalid input.
 * Method:
 * 1. Track whether an increase and a decrease appeared.
 * 2. Return 2 if both appear.
 * 3. Otherwise return 1, -1, or 0.
 */
int32_t array_monotonic_direction(const int32_t *values, uint32_t count) {
  if (!values && count) return 2;
  int increased = 0, decreased = 0;
  for (uint32_t i = 1; i < count; ++i) {
    increased |= values[i] > values[i - 1];
    decreased |= values[i] < values[i - 1];
    if (increased && decreased) return 2;
  }
  return increased ? 1 : decreased ? -1 : 0;
}

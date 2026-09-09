#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Produce adjacent differences
 * Contract: Write values[i+1]-values[i] as signed 64-bit results. Output length is count-1 for nonempty input and zero for empty input. Validate all inputs before writing.
 * Method:
 * 1. Compute the required output count.
 * 2. Load neighboring values.
 * 3. Widen before subtracting.
 * 4. Store each 64-bit difference.
 */
int array_adjacent_differences(const int32_t *values, uint32_t count,
                               int64_t *output, uint32_t capacity) {
  uint32_t needed = count ? count - 1 : 0;
  if (capacity < needed || (!values && count) || (!output && needed)) return 0;
  for (uint32_t i = 0; i < needed; ++i)
    output[i] = (int64_t)values[i + 1] - values[i];
  return 1;
}

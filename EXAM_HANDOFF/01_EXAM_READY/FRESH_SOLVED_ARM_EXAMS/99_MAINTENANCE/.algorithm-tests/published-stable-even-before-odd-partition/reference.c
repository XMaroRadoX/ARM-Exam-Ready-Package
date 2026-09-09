#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Partition even values before odd values stably
 * Contract: Move even values before odd values while preserving order within both
 * groups. The in-place insertion method uses no scratch buffer. Method:
 * 1. Scan left to right.
 * 2. Save an even value that follows odds.
 * 3. Shift the odd block right.
 * 4. Insert the saved even value.
 */
int array_stable_even_first(int32_t *values, uint32_t count) {
  if (!values && count)
    return 0;
  for (uint32_t i = 1; i < count; ++i) {
    if ((values[i] & 1) == 0) {
      int32_t even = values[i];
      uint32_t j = i;
      while (j && (values[j - 1] & 1)) {
        values[j] = values[j - 1];
        --j;
      }
      values[j] = even;
    }
  }
  return 1;
}

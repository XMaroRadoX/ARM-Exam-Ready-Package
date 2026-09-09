#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Count zero array values
 * Contract: Count matching signed words. A null pointer returns zero; the routine never
 * writes memory. Method:
 * 1. Start the count at zero.
 * 2. Test each element against the requested condition.
 * 3. Increment exactly once for each match.
 */
uint32_t count_array_zero(const int32_t *values, uint32_t count) {
  uint32_t matches = 0;
  if (!values)
    return 0;
  for (uint32_t i = 0; i < count; ++i)
    if (values[i] == 0)
      ++matches;
  return matches;
}

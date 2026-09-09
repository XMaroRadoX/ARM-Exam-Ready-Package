#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Find the maximum array value
 * Contract: Return the maximum signed value. Empty input or a null required pointer returns 0 without writing. Equal values keep the first candidate.
 * Method:
 * 1. Seed the candidate from element zero.
 * 2. Scan remaining elements with signed comparisons.
 * 3. Replace it only for a strict improvement.
 */
int array_maximum(const int32_t *values, uint32_t count,
                 int32_t *value_out) {
  if (!values || !value_out || count == 0) return 0;
  int32_t best = values[0];
  for (uint32_t i = 1; i < count; ++i)
    if (values[i] > best) best = values[i];
  *value_out = best;
  return 1;
}

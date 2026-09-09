#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Checked array sum
 * Contract: Sum signed words into a 64-bit result. count must not exceed INT32_MAX, which guarantees that every possible int32_t input sum fits int64_t. A zero-length array sums to zero and may have a null data pointer. Return 0 without writing for an invalid pointer or count.
 * Method:
 * 1. Validate the output and count bound.
 * 2. Start a 64-bit accumulator at zero.
 * 3. Sign-extend and add each word.
 * 4. Store only after the complete scan.
 */
int checked_array_sum(const int32_t *values, uint32_t count,
                      int64_t *sum_out) {
  /* INT32_MAX elements cannot overflow a signed 64-bit sum. */
  if (!sum_out || count > INT32_MAX || (!values && count != 0)) return 0;
  int64_t sum = 0;
  for (uint32_t i = 0; i < count; ++i) sum += values[i];
  *sum_out = sum;
  return 1;
}

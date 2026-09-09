#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Subtract signed integers with overflow detection
 * Contract: Return 1 and the exact signed 32-bit result. Return 0 without writing when result_out is null or the mathematical result is outside INT32_MIN..INT32_MAX.
 * Method:
 * 1. Compute a widened result or inspect the ARM overflow condition.
 * 2. Reject overflow before storing.
 * 3. Publish the result only on success.
 */
int checked_subtract_i32(int32_t left, int32_t right, int32_t *result_out) {
  if (!result_out) return 0;
  int64_t wide=(int64_t)left - right;
  if (wide<INT32_MIN || wide>INT32_MAX) return 0;
  *result_out=(int32_t)wide;
  return 1;
}

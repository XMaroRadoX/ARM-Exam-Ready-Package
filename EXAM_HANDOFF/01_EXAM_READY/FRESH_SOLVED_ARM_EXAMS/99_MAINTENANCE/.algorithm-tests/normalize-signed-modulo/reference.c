#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Normalize signed modulo into a nonnegative result
 * Contract: Require modulus>0. Return the unique result in 0..modulus-1 that is congruent to value. Invalid input returns 0 without writing.
 * Method:
 * 1. Calculate the C signed remainder.
 * 2. Add modulus if the remainder is negative.
 * 3. Store the normalized result.
 */
int normalized_modulo_i32(int32_t value, int32_t modulus,
                          int32_t *result_out) {
  if (!result_out || modulus<=0) return 0;
  int32_t result=value%modulus;
  if(result<0) result+=modulus;
  *result_out=result;
  return 1;
}

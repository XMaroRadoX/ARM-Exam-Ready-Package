#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Find the next power of two with overflow detection
 * Contract: Return the smallest power of two greater than or equal to value. Define
 * input zero as result one. Values above 0x80000000 cannot be represented and fail
 * without writing. Method:
 * 1. Handle zero and reject the overflow range.
 * 2. Subtract one.
 * 3. Spread the highest set bit downward.
 * 4. Add one.
 */
int next_power_of_two_u32(uint32_t value, uint32_t *result_out) {
  if (!result_out || value > 0x80000000u)
    return 0;
  if (value == 0)
    value = 1;
  else {
    --value;
    value |= value >> 1;
    value |= value >> 2;
    value |= value >> 4;
    value |= value >> 8;
    value |= value >> 16;
    ++value;
  }
  *result_out = value;
  return 1;
}

#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Test whether an integer is a power of two
 * Contract: Return 1 only for positive unsigned values containing exactly one set bit.
 * Zero is not a power of two. Method:
 * 1. Reject zero.
 * 2. Clear the lowest set bit with value & (value-1).
 * 3. A zero remainder means exactly one bit was set.
 */
int is_power_of_two_u32(uint32_t value) {
  return value != 0 && (value & (value - 1u)) == 0;
}

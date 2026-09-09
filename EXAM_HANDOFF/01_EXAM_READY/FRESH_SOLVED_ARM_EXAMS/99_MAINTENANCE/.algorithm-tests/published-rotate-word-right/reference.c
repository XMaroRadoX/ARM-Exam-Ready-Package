#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Rotate a 32-bit word right
 * Contract: Normalize amount modulo 32 and rotate without losing bits. A zero or
 * multiple-of-32 amount returns the original word. Method:
 * 1. Keep the low five amount bits.
 * 2. Combine opposite logical shifts in C.
 * 3. Use the ARM rotate instruction with the equivalent direction.
 */
uint32_t rotate_right_u32(uint32_t value, uint32_t amount) {
  amount &= 31u;
  return amount ? (value >> amount) | (value << (32u - amount)) : value;
}

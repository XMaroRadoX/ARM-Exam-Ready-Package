#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Reverse the byte order of a 32-bit word
 * Contract: Return the same four bytes in reverse order. This changes logical byte
 * positions and does not access memory. Method:
 * 1. Extract or route each byte to the opposite position.
 * 2. Combine all four non-overlapping fields.
 */
uint32_t reverse_byte_order_u32(uint32_t value) {
  return ((value & 0x000000ffu) << 24) | ((value & 0x0000ff00u) << 8) |
         ((value & 0x00ff0000u) >> 8) | ((value & 0xff000000u) >> 24);
}

#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Swap the two nibbles of a byte
 * Contract: Exchange bits 7..4 with bits 3..0 and return the low eight-bit result.
 * Method:
 * 1. Shift the low nibble left four.
 * 2. Shift the high nibble right four.
 * 3. OR the two fields.
 */
uint8_t swap_byte_nibbles(uint8_t value) {
  return (uint8_t)((value << 4) | (value >> 4));
}

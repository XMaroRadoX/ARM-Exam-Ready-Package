#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Unpack a 32-bit word into four bytes
 * Contract: Write bits 31..24, 23..16, 15..8, and 7..0 into output[0..3]. Require capacity>=4 and a valid output; failure writes nothing.
 * Method:
 * 1. Validate all output storage.
 * 2. Shift each declared field to the low byte.
 * 3. Store exactly four bytes.
 */
int unpack_four_bytes_be(uint32_t value, uint8_t *output,
                         uint32_t capacity) {
  if(!output || capacity<4) return 0;
  output[0]=(uint8_t)(value>>24);
  output[1]=(uint8_t)(value>>16);
  output[2]=(uint8_t)(value>>8);
  output[3]=(uint8_t)value;
  return 1;
}

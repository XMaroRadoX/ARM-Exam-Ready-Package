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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int unpack_four_bytes_be(uint32_t value, uint8_t *output, uint32_t capacity);
int test_main(void) {
uint8_t o[5]={0};o[4]=77;CHECK(unpack_four_bytes_be(0x12345678u,o,4));
CHECK(o[0]==0x12&&o[1]==0x34&&o[2]==0x56&&o[3]==0x78&&o[4]==77);
o[0]=99;CHECK(!unpack_four_bytes_be(0, o,3)&&o[0]==99);
CHECK(!unpack_four_bytes_be(0,0,4));
return 0;
}

int main(void){return test_main();}

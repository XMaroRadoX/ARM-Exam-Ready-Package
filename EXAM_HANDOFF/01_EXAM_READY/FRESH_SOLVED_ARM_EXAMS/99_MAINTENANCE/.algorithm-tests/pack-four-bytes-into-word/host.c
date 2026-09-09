#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Pack four bytes into a 32-bit word
 * Contract: Pack first into bits 31..24, second into 23..16, third into 15..8, and fourth into 7..0. The name describes this logical big-endian display order; no memory access occurs.
 * Method:
 * 1. Mask each input to eight bits.
 * 2. Shift it to its declared field.
 * 3. OR the four disjoint fields.
 */
uint32_t pack_four_bytes_be(uint8_t first, uint8_t second,
                            uint8_t third, uint8_t fourth) {
  return ((uint32_t)first<<24)|((uint32_t)second<<16)|
         ((uint32_t)third<<8)|fourth;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t pack_four_bytes_be(uint8_t first, uint8_t second,
                            uint8_t third, uint8_t fourth);
int test_main(void) {
CHECK(pack_four_bytes_be(0x12,0x34,0x56,0x78)==0x12345678u);
CHECK(pack_four_bytes_be(0,0,0,0)==0);
CHECK(pack_four_bytes_be(0xff,0xff,0xff,0xff)==UINT32_MAX);
return 0;
}

int main(void){return test_main();}

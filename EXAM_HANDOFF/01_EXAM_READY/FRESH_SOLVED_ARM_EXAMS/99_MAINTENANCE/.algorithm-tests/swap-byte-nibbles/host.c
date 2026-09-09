#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Swap the two nibbles of a byte
 * Contract: Exchange bits 7..4 with bits 3..0 and return the low eight-bit result.
 * Method:
 * 1. Shift the low nibble left four.
 * 2. Shift the high nibble right four.
 * 3. OR the two fields.
 */
uint8_t swap_byte_nibbles(uint8_t value) {
  return (uint8_t)((value<<4)|(value>>4));
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint8_t swap_byte_nibbles(uint8_t value);
int test_main(void) {
CHECK(swap_byte_nibbles(0xabu)==0xbau);
CHECK(swap_byte_nibbles(0x10u)==0x01u);
CHECK(swap_byte_nibbles(0xffu)==0xffu);
return 0;
}

int main(void){return test_main();}

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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t reverse_byte_order_u32(uint32_t value);
int test_main(void) {
  CHECK(reverse_byte_order_u32(0x12345678u) == 0x78563412u);
  CHECK(reverse_byte_order_u32(0) == 0);
  CHECK(reverse_byte_order_u32(0xaabbccddu) == 0xddccbbaau);
  return 0;
}

int main(void){return test_main();}

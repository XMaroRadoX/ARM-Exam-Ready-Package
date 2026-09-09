#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t reverse_byte_order_u32(uint32_t value);
int test_main(void) {
  CHECK(reverse_byte_order_u32(0x12345678u) == 0x78563412u);
  CHECK(reverse_byte_order_u32(0) == 0);
  CHECK(reverse_byte_order_u32(0xaabbccddu) == 0xddccbbaau);
  return 0;
}

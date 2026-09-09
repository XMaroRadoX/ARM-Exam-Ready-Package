#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t rotate_right_u32(uint32_t value, uint32_t amount);
int test_main(void) {
  CHECK(rotate_right_u32(0x12345678u, 4) == 0x81234567u);
  CHECK(rotate_right_u32(0x12345678u, 0) == 0x12345678u);
  CHECK(rotate_right_u32(0x12345678u, 36) == 0x81234567u);
  return 0;
}

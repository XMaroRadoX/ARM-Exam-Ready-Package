#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t pack_four_bytes_be(uint8_t first, uint8_t second, uint8_t third,
                            uint8_t fourth);
int test_main(void) {
  CHECK(pack_four_bytes_be(0x12, 0x34, 0x56, 0x78) == 0x12345678u);
  CHECK(pack_four_bytes_be(0, 0, 0, 0) == 0);
  CHECK(pack_four_bytes_be(0xff, 0xff, 0xff, 0xff) == UINT32_MAX);
  return 0;
}

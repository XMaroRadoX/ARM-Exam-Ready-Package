#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int unpack_four_bytes_be(uint32_t value, uint8_t *output, uint32_t capacity);
int test_main(void) {
  uint8_t o[5] = {0};
  o[4] = 77;
  CHECK(unpack_four_bytes_be(0x12345678u, o, 4));
  CHECK(o[0] == 0x12 && o[1] == 0x34 && o[2] == 0x56 && o[3] == 0x78 && o[4] == 77);
  o[0] = 99;
  CHECK(!unpack_four_bytes_be(0, o, 3) && o[0] == 99);
  CHECK(!unpack_four_bytes_be(0, 0, 4));
  return 0;
}

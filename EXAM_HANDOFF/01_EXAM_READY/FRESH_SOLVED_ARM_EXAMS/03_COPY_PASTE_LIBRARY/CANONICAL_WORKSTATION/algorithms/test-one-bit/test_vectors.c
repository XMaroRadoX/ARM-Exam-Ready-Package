#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int test_bit_u32(uint32_t value, uint32_t index, uint32_t *result_out);
int test_main(void) {
  uint32_t out = 77;
  CHECK(test_bit_u32(0x80000008u, 31, &out) && out == 1);
  out = 77;
  CHECK(!test_bit_u32(8, 32, &out) && out == 77);
  CHECK(!test_bit_u32(8, 3, 0));
  return 0;
}

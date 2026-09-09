#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int next_power_of_two_u32(uint32_t value, uint32_t *result_out);
int test_main(void) {
  uint32_t out = 77;
  CHECK(next_power_of_two_u32(13, &out) && out == 16);
  CHECK(next_power_of_two_u32(0, &out) && out == 1);
  CHECK(next_power_of_two_u32(0x80000000u, &out) && out == 0x80000000u);
  out = 77;
  CHECK(!next_power_of_two_u32(0x80000001u, &out) && out == 77);
  return 0;
}

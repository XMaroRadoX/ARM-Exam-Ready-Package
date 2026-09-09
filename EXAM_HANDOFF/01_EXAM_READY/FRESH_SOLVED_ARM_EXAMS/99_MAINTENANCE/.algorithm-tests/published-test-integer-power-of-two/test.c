#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int is_power_of_two_u32(uint32_t value);
int test_main(void) {
  CHECK(is_power_of_two_u32(1));
  CHECK(is_power_of_two_u32(16));
  CHECK(is_power_of_two_u32(0) == 0);
  CHECK(is_power_of_two_u32(18) == 0);
  CHECK(is_power_of_two_u32(0x80000000u));
  return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int packed_bcd(uint32_t value, uint32_t *out);
int test_main(void) {
  uint32_t v = 0;
  CHECK(packed_bcd(12345678, &v) && v == 0x12345678);
  CHECK(packed_bcd(42, &v) && v == 0x42);
  CHECK(packed_bcd(0, &v) && v == 0);
  v = 99;
  CHECK(!packed_bcd(100000000, &v) && v == 99);
  return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int modular_power(uint32_t base, uint32_t exponent, uint32_t modulus, uint32_t *out);
int test_main(void) {
  uint32_t v = 9;
  CHECK(modular_power(3, 5, 7, &v) && v == 5);
  CHECK(modular_power(2, 0, 1, &v) && v == 0);
  CHECK(!modular_power(3, 2, 0, &v));
  CHECK(modular_power(65534, 2, 65535, &v) && v == 1);
  return 0;
}

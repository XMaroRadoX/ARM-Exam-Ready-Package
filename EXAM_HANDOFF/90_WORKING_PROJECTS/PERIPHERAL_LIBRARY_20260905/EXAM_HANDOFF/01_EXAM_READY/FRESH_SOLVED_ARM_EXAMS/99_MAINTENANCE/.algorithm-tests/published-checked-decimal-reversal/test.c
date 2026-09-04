#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int reverse_decimal(uint32_t n, uint32_t *out);
int test_main(void) {
  uint32_t v = 7;
  CHECK(reverse_decimal(1203, &v) && v == 3021);
  CHECK(reverse_decimal(0, &v) && v == 0);
  v = 99;
  CHECK(!reverse_decimal(4294967295u, &v) && v == 99);
  CHECK(reverse_decimal(123321, &v) && v == 123321);
  return 0;
}

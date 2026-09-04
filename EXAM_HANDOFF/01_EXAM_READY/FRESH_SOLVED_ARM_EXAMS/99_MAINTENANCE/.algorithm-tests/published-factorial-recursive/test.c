#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int factorial_recursive(uint32_t n, uint32_t *out);
int test_main(void) {
  uint32_t v = 0;
  CHECK(factorial_recursive(0, &v) && v == 1);
  CHECK(factorial_recursive(3, &v) && v == 6);
  CHECK(factorial_recursive(12, &v) && v == 479001600);
  CHECK(!factorial_recursive(13, &v));
  return 0;
}

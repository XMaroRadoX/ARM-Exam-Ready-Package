#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int factorial_iterative(uint32_t n, uint32_t *out);
int test_main(void) {
  uint32_t v = 99;
  CHECK(factorial_iterative(0, &v) && v == 1);
  CHECK(factorial_iterative(4, &v) && v == 24);
  CHECK(factorial_iterative(12, &v) && v == 479001600);
  CHECK(!factorial_iterative(13, &v) && v == 479001600);
  return 0;
}

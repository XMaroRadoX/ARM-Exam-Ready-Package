#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int binomial_coefficient(uint32_t n, uint32_t k, uint32_t *out);
int test_main(void) {
  uint32_t v = 0;
  CHECK(binomial_coefficient(5, 2, &v) && v == 10);
  CHECK(binomial_coefficient(30, 15, &v) && v == 155117520);
  CHECK(binomial_coefficient(0, 0, &v) && v == 1);
  CHECK(!binomial_coefficient(31, 1, &v));
  return 0;
}

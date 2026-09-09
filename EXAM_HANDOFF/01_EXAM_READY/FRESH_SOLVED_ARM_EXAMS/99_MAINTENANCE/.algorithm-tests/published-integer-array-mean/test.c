#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int integer_array_mean(const int32_t *values, uint32_t count, int32_t *mean_out);
int test_main(void) {
  int32_t a[] = {-8, 3, 4}, b[] = {INT32_MAX, INT32_MAX}, m = 77;
  CHECK(integer_array_mean(a, 3, &m) && m == 0);
  CHECK(integer_array_mean(b, 2, &m) && m == INT32_MAX);
  m = 77;
  CHECK(!integer_array_mean(a, 0, &m) && m == 77);
  CHECK(!integer_array_mean(0, 3, &m) && m == 77);
  return 0;
}

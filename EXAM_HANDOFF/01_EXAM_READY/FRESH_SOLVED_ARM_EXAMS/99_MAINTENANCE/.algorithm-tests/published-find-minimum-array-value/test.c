#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_minimum(const int32_t *values, uint32_t count, int32_t *value_out);
int test_main(void) {
  int32_t a[] = {7, -3, 9, -3}, v = 77;
  CHECK(array_minimum(a, 4, &v) && v == -3);
  v = 77;
  CHECK(!array_minimum(a, 0, &v) && v == 77);
  CHECK(!array_minimum(0, 1, &v) && v == 77);
  return 0;
}

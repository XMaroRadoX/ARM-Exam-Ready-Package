#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int second_largest(const int32_t *a, uint32_t n, int32_t *out);
int test_main(void) {
  int32_t a[] = {4, 9, 9, 2}, e[] = {INT32_MIN, INT32_MAX}, v = 77;
  CHECK(second_largest(a, 4, &v) && v == 4);
  CHECK(second_largest(e, 2, &v) && v == INT32_MIN);
  v = 77;
  CHECK(!second_largest(a, 1, &v) && v == 77);
  CHECK(!second_largest(0, 0, &v));
  return 0;
}

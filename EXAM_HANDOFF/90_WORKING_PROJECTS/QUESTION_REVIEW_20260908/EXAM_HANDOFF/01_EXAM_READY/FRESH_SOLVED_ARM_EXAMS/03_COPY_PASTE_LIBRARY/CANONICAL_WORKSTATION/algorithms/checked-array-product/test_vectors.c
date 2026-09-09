#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int checked_array_product(const int32_t *values, uint32_t count, int32_t *product_out);
int test_main(void) {
  int32_t a[] = {-2, 3, 4}, b[] = {INT32_MAX, 2}, p = 77;
  CHECK(checked_array_product(a, 3, &p) && p == -24);
  CHECK(checked_array_product(0, 0, &p) && p == 1);
  p = 77;
  CHECK(!checked_array_product(b, 2, &p) && p == 77);
  CHECK(!checked_array_product(0, 1, &p) && p == 77);
  return 0;
}

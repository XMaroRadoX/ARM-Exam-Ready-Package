#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int majority_element(const int32_t *a, uint32_t n, int32_t *out);
int test_main(void) {
  int32_t a[] = {2, 1, 2, 3, 2}, b[] = {1, 2, 3, 4}, v = 99;
  CHECK(majority_element(a, 5, &v) && v == 2);
  v = 99;
  CHECK(!majority_element(b, 4, &v) && v == 99);
  CHECK(!majority_element(0, 0, &v));
  return 0;
}

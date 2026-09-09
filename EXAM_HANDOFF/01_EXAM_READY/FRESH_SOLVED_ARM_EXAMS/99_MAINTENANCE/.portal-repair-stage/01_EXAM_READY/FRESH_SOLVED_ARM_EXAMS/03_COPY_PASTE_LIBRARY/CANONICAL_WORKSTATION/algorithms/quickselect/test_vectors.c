#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int quickselect(int *a, size_t n, size_t k, int *out);
int test_main(void) {
  int a[] = {4, 1, 3, 2}, v = 0;
  CHECK(quickselect(a, 4, 1, &v) && v == 2);
  int b[] = {2, 2, 2};
  CHECK(quickselect(b, 3, 2, &v) && v == 2);
  CHECK(!quickselect(a, 4, 4, &v));
  return 0;
}

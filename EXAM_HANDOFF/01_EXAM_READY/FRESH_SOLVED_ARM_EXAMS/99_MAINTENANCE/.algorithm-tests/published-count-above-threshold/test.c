#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t count_above(const int32_t *a, uint32_t n, int32_t threshold);
int test_main(void) {
  int32_t a[] = {-3, 0, 4, 4};
  CHECK(count_above(a, 4, 0) == 2);
  CHECK(count_above(a, 4, INT32_MAX) == 0);
  CHECK(count_above(0, 0, 0) == 0);
  return 0;
}

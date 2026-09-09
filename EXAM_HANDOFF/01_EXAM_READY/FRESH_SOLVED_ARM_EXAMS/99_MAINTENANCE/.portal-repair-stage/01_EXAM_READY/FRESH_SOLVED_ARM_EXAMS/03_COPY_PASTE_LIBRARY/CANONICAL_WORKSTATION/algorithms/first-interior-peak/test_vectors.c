#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t first_peak(const int32_t *a, uint32_t n);
int test_main(void) {
  int32_t a[] = {1, 4, 2, 5, 1}, b[] = {1, 2, 2, 1};
  CHECK(first_peak(a, 5) == 1);
  CHECK(first_peak(b, 4) == -1);
  CHECK(first_peak(a, 2) == -1);
  return 0;
}

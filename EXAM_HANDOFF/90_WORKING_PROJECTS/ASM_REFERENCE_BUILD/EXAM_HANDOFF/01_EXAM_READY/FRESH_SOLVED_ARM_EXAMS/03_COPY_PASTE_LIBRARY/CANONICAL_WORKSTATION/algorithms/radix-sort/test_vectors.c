#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int radix_sort_u32(uint32_t *a, size_t n, uint32_t *tmp);
int test_main(void) {
  uint32_t a[] = {256, 1, UINT32_MAX, 0, 1}, t[5];
  CHECK(radix_sort_u32(a, 5, t) && a[0] == 0 && a[1] == 1 && a[2] == 1 && a[3] == 256 &&
        a[4] == UINT32_MAX);
  CHECK(radix_sort_u32(0, 0, 0));
  CHECK(!radix_sort_u32(a, 5, a));
  return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int extrema_indexes(const int32_t *a, uint32_t n, uint32_t *min_index,
                    uint32_t *max_index);
int test_main(void) {
  int32_t a[] = {7, -2, 7, -2};
  uint32_t l = 99, h = 99;
  CHECK(extrema_indexes(a, 4, &l, &h) && l == 1 && h == 0);
  CHECK(!extrema_indexes(a, 0, &l, &h) && l == 1 && h == 0);
  return 0;
}

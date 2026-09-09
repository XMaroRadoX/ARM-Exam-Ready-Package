#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_swap_indexes(int32_t *values, uint32_t count, uint32_t first,
                       uint32_t second);
int test_main(void) {
  int32_t a[] = {4, 5, 6, 7};
  CHECK(array_swap_indexes(a, 4, 1, 3));
  CHECK(a[0] == 4 && a[1] == 7 && a[2] == 6 && a[3] == 5);
  CHECK(array_swap_indexes(a, 4, 2, 2));
  CHECK(!array_swap_indexes(a, 4, 0, 4));
  return 0;
}

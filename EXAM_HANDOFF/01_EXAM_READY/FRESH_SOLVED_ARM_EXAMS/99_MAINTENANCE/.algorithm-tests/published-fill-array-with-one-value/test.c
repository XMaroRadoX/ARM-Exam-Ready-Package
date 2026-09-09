#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_fill(int32_t *values, uint32_t count, int32_t fill_value);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 77};
  CHECK(array_fill(a, 4, -3));
  CHECK(a[0] == -3 && a[3] == -3 && a[4] == 77);
  CHECK(array_fill(0, 0, 9));
  CHECK(!array_fill(0, 1, 9));
  return 0;
}

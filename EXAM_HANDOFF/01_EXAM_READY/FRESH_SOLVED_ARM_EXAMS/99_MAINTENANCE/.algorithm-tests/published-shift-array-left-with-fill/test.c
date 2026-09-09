#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_shift_left(int32_t *values, uint32_t count, uint32_t amount,
                     int32_t fill_value);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 77};
  CHECK(array_shift_left(a, 4, 2, -1));
  CHECK(a[0] == 3 && a[1] == 4 && a[2] == -1 && a[3] == -1 && a[4] == 77);
  CHECK(array_shift_left(a, 4, 9, 5) && a[0] == 5 && a[3] == 5);
  CHECK(array_shift_left(0, 0, 1, 5));
  CHECK(!array_shift_left(0, 1, 1, 5));
  return 0;
}

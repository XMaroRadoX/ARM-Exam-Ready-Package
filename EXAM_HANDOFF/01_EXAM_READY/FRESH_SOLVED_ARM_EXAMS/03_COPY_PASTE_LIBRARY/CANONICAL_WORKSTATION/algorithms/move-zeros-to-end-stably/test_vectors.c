#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_move_zeros_to_end(int32_t *values, uint32_t count);
int test_main(void) {
  int32_t a[] = {0, 4, 0, -2, 7, 77};
  CHECK(array_move_zeros_to_end(a, 5));
  CHECK(a[0] == 4 && a[1] == -2 && a[2] == 7 && a[3] == 0 && a[4] == 0 && a[5] == 77);
  CHECK(array_move_zeros_to_end(0, 0));
  CHECK(!array_move_zeros_to_end(0, 1));
  return 0;
}

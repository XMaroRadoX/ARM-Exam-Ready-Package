#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t array_monotonic_direction(const int32_t *values, uint32_t count);
int test_main(void) {
  int32_t a[] = {5, 5, 3, 1}, b[] = {1, 4, 2}, c[] = {7, 7};
  CHECK(array_monotonic_direction(a, 4) == -1);
  CHECK(array_monotonic_direction(b, 3) == 2);
  CHECK(array_monotonic_direction(c, 2) == 0);
  CHECK(array_monotonic_direction(0, 0) == 0);
  return 0;
}

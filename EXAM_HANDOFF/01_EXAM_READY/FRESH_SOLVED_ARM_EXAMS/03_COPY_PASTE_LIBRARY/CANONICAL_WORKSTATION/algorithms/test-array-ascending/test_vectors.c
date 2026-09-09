#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_is_ascending(const int32_t *values, uint32_t count);
int test_main(void) {
  int32_t a[] = {-3, -3, 4, 9}, b[] = {-3, 4, 2};
  CHECK(array_is_ascending(a, 4));
  CHECK(!array_is_ascending(b, 3));
  CHECK(array_is_ascending(0, 0));
  CHECK(!array_is_ascending(0, 1));
  return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_adjacent_differences(const int32_t *values, uint32_t count, int64_t *output,
                               uint32_t capacity);
int test_main(void) {
  int32_t a[] = {INT32_MIN, 0, INT32_MAX};
  int64_t o[3] = {0};
  o[2] = 77;
  CHECK(array_adjacent_differences(a, 3, o, 2));
  CHECK(o[0] == 2147483648LL && o[1] == 2147483647LL && o[2] == 77);
  CHECK(array_adjacent_differences(0, 0, 0, 0));
  o[0] = 99;
  CHECK(!array_adjacent_differences(a, 3, o, 1) && o[0] == 99);
  return 0;
}

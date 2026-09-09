#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int checked_subtract_i32(int32_t left, int32_t right, int32_t *result_out);
int test_main(void) {
  int32_t out = 77;
  CHECK(checked_subtract_i32(20, 7, &out) && out == 13);
  out = 77;
  CHECK(!checked_subtract_i32(INT32_MIN, 1, &out) && out == 77);
  CHECK(!checked_subtract_i32(1, 2, 0));
  return 0;
}

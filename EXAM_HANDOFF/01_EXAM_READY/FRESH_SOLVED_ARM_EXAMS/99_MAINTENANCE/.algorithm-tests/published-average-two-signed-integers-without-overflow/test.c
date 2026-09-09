#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t average_two_i32(int32_t left, int32_t right);
int test_main(void) {
  CHECK(average_two_i32(INT32_MIN, INT32_MAX) == 0);
  CHECK(average_two_i32(INT32_MAX, INT32_MAX) == INT32_MAX);
  CHECK(average_two_i32(-8, -5) == -6);
  CHECK(average_two_i32(8, 5) == 6);
  return 0;
}

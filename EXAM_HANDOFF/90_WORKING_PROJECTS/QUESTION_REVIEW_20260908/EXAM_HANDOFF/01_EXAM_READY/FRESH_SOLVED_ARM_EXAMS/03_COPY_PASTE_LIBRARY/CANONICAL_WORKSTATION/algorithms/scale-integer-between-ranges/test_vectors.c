#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int scale_i32_between_ranges(int32_t value, int32_t input_min, int32_t input_max,
                             int32_t output_min, int32_t output_max,
                             int32_t *result_out);
int test_main(void) {
  int32_t out = 77;
  CHECK(scale_i32_between_ranges(25, 0, 100, 0, 1000, &out) && out == 250);
  CHECK(scale_i32_between_ranges(120, 0, 100, 0, 1000, &out) && out == 1000);
  CHECK(scale_i32_between_ranges(25, 0, 100, 1000, 0, &out) && out == 750);
  out = 77;
  CHECK(!scale_i32_between_ranges(2, 5, 5, 0, 10, &out) && out == 77);
  CHECK(!scale_i32_between_ranges(2, 0, 5, 0, 10, 0));
  return 0;
}

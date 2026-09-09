#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int decimal_digit_frequency_i32(int32_t value, uint32_t counts[10]);
int test_main(void) {
  uint32_t c[11];
  for (unsigned i = 0; i < 11; i++)
    c[i] = 77;
  CHECK(decimal_digit_frequency_i32(-12012, c));
  CHECK(c[0] == 1 && c[1] == 2 && c[2] == 2 && c[3] == 0 && c[10] == 77);
  CHECK(decimal_digit_frequency_i32(0, c) && c[0] == 1 && c[1] == 0);
  CHECK(decimal_digit_frequency_i32(INT32_MIN, c) && c[2] == 1 && c[8] == 2);
  CHECK(!decimal_digit_frequency_i32(5, 0));
  return 0;
}

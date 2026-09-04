#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t decimal_digit_count(uint32_t n);
int test_main(void) {
  CHECK(decimal_digit_count(12034) == 5);
  CHECK(decimal_digit_count(0) == 1);
  CHECK(decimal_digit_count(123) == 3);
  return 0;
}

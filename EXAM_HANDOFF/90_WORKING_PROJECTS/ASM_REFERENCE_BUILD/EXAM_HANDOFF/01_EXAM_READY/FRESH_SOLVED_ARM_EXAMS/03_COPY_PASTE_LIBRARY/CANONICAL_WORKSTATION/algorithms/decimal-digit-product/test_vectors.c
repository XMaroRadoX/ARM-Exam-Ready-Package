#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t decimal_digit_product(uint32_t n);
int test_main(void) {
  CHECK(decimal_digit_product(12034) == 0);
  CHECK(decimal_digit_product(0) == 0);
  CHECK(decimal_digit_product(123) == 6);
  return 0;
}

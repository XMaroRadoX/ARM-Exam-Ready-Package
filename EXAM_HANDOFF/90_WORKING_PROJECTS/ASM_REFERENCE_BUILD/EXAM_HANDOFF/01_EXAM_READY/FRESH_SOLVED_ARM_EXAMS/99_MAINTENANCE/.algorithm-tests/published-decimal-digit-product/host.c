#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t decimal_digit_product(uint32_t n) {
  uint32_t v = 1;
  do {
    uint32_t d = n % 10;
    (void)d;
    v *= d;
    n /= 10;
  } while (n);
  return v;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t decimal_digit_product(uint32_t n);
int test_main(void) {
  CHECK(decimal_digit_product(12034) == 0);
  CHECK(decimal_digit_product(0) == 0);
  CHECK(decimal_digit_product(123) == 6);
  return 0;
}

int main(void){return test_main();}

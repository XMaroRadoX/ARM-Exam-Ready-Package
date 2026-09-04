#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int digit_sum_base(uint32_t n, uint32_t b, uint32_t *out) {
  if (b < 2 || b > 36 || !out)
    return 0;
  uint32_t s = 0;
  do {
    s += n % b;
    n /= b;
  } while (n);
  *out = s;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int digit_sum_base(uint32_t n, uint32_t base, uint32_t *out);
int test_main(void) {
  uint32_t v = 8;
  CHECK(digit_sum_base(31, 16, &v) && v == 16);
  CHECK(digit_sum_base(0xffffffffu, 2, &v) && v == 32);
  CHECK(!digit_sum_base(3, 1, &v));
  return 0;
}

int main(void){return test_main();}

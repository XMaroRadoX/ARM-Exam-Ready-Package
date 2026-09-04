#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int reverse_decimal(uint32_t n, uint32_t *out) {
  if (!out)
    return 0;
  uint64_t v = 0;
  do {
    v = v * 10 + n % 10;
    if (v > UINT32_MAX)
      return 0;
    n /= 10;
  } while (n);
  *out = (uint32_t)v;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int reverse_decimal(uint32_t n, uint32_t *out);
int test_main(void) {
  uint32_t v = 7;
  CHECK(reverse_decimal(1203, &v) && v == 3021);
  CHECK(reverse_decimal(0, &v) && v == 0);
  v = 99;
  CHECK(!reverse_decimal(4294967295u, &v) && v == 99);
  CHECK(reverse_decimal(123321, &v) && v == 123321);
  return 0;
}

int main(void){return test_main();}

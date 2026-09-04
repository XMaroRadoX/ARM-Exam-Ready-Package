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

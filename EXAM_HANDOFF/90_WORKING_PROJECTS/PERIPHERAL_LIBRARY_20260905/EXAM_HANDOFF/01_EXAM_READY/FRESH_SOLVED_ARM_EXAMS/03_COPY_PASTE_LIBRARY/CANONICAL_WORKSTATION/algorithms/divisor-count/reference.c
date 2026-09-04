#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t divisor_count(uint32_t n) {
  uint32_t c = 0;
  for (uint32_t d = 1; n && d <= n / d; d++)
    if (n % d == 0)
      c += d == n / d ? 1 : 2;
  return c;
}

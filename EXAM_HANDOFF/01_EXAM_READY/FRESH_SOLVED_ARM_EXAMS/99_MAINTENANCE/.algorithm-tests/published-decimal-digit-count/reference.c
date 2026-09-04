#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t decimal_digit_count(uint32_t n) {
  uint32_t v = 0;
  do {
    uint32_t d = n % 10;
    (void)d;
    v++;
    n /= 10;
  } while (n);
  return v;
}

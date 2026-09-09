#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int armstrong_number(uint32_t n) {
  uint32_t k = 0, x = n;
  do {
    k++;
    x /= 10;
  } while (x);
  uint64_t s = 0;
  x = n;
  do {
    uint32_t d = x % 10;
    uint64_t p = 1;
    for (uint32_t i = 0; i < k; i++)
      p *= d;
    s += p;
    x /= 10;
  } while (x);
  return s == n;
}

#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t trailing_zero_count(uint32_t v) {
  if (!v)
    return 32;
  uint32_t n = 0;
  while (!(v & 1u)) {
    n++;
    v >>= 1;
  }
  return n;
}

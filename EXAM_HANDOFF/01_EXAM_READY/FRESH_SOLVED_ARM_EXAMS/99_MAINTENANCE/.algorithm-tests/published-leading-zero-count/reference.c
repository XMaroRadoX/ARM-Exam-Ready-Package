#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t leading_zero_count(uint32_t v) {
  if (!v)
    return 32;
  uint32_t n = 0;
  while (!(v & 0x80000000u)) {
    n++;
    v <<= 1;
  }
  return n;
}

#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint64_t array_bit_differences(const uint32_t *a, const uint32_t *b, uint32_t n) {
  uint64_t s = 0;
  if (a && b)
    for (uint32_t i = 0; i < n; i++) {
      uint32_t x = a[i] ^ b[i];
      while (x) {
        s++;
        x &= x - 1;
      }
    }
  return s;
}

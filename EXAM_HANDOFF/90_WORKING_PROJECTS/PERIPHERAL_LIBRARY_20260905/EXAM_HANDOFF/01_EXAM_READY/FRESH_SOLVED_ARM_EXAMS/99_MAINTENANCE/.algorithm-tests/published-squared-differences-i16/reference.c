#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint64_t squared_differences_i16(const int16_t *a, const int16_t *b, uint32_t n) {
  uint64_t s = 0;
  if (a && b)
    for (uint32_t i = 0; i < n; i++) {
      int64_t d = (int32_t)a[i] - b[i];
      s += (uint64_t)(d * d);
    }
  return s;
}

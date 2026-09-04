#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int extrema_indexes(const int32_t *a, uint32_t n, uint32_t *lo, uint32_t *hi) {
  if (!a || !n || !lo || !hi || lo == hi)
    return 0;
  uint32_t l = 0, h = 0;
  for (uint32_t i = 1; i < n; i++) {
    if (a[i] < a[l])
      l = i;
    if (a[i] > a[h])
      h = i;
  }
  *lo = l;
  *hi = h;
  return 1;
}

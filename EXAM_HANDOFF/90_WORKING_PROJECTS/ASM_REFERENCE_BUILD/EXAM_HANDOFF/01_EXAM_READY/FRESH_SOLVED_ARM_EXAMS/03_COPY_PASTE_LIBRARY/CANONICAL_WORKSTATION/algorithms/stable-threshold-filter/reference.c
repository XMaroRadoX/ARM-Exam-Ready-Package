#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t threshold_filter(const int32_t *a, uint32_t n, int32_t t, int32_t *out,
                          uint32_t cap) {
  if (cap < n || ((!a || !out) && n))
    return UINT32_MAX;
  uint32_t k = 0;
  for (uint32_t i = 0; i < n; i++)
    if (a[i] > t)
      out[k++] = a[i];
  return k;
}

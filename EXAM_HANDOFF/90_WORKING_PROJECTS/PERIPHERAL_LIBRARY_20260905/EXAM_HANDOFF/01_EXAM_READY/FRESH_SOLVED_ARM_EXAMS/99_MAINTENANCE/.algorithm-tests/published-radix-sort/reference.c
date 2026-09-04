#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int radix_sort_u32(uint32_t *a, size_t n, uint32_t *tmp) {
  if (!n)
    return 1;
  if (!a || !tmp || a == tmp)
    return 0;
  size_t count[256];
  for (unsigned shift = 0; shift < 32; shift += 8) {
    for (size_t b = 0; b < 256; b++)
      count[b] = 0;
    for (size_t i = 0; i < n; i++)
      count[(a[i] >> shift) & 255]++;
    size_t sum = 0;
    for (size_t b = 0; b < 256; b++) {
      size_t c = count[b];
      count[b] = sum;
      sum += c;
    }
    for (size_t i = 0; i < n; i++) {
      unsigned b = (a[i] >> shift) & 255;
      tmp[count[b]++] = a[i];
    }
    for (size_t i = 0; i < n; i++)
      a[i] = tmp[i];
  }
  return 1;
}

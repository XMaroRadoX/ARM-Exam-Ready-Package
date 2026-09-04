#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t rle_decode(const uint8_t *p, uint32_t n, uint8_t *out, uint32_t cap) {
  if ((!p && n) || n > UINT32_MAX / 2)
    return UINT32_MAX;
  uint32_t total = 0;
  for (uint32_t i = 0; i < n; i++) {
    uint32_t c = p[2 * i];
    if (!c || total > UINT32_MAX - c)
      return UINT32_MAX;
    total += c;
  }
  if (total > cap || (!out && total))
    return UINT32_MAX;
  uint32_t k = 0;
  for (uint32_t i = 0; i < n; i++)
    for (uint32_t j = 0; j < p[2 * i]; j++)
      out[k++] = p[2 * i + 1];
  return k;
}

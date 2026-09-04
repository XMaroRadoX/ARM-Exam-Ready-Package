#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_sums(const int16_t *a, uint32_t r, uint32_t c, int64_t *out, uint32_t cap) {
  if (!a || !out || !r || !c || r > 256 || c > 256 || cap < r + c)
    return 0;
  for (uint32_t i = 0; i < r; i++) {
    int32_t s = 0;
    for (uint32_t j = 0; j < c; j++)
      s += a[i * c + j];
    out[i] = s;
  }
  for (uint32_t j = 0; j < c; j++) {
    int32_t s = 0;
    for (uint32_t i = 0; i < r; i++)
      s += a[i * c + j];
    out[r + j] = s;
  }
  return 1;
}

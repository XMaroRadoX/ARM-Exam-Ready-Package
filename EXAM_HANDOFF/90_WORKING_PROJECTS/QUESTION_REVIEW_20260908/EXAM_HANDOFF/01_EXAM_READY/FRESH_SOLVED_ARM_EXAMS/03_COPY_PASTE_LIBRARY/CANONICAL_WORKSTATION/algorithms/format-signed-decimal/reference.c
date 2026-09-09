#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t format_i32(int32_t v, char *out, uint32_t cap) {
  char d[12];
  uint32_t x = v < 0 ? (uint32_t)(-(int64_t)v) : (uint32_t)v, n = 0, k = 0;
  do {
    d[n++] = (char)(48 + x % 10);
    x /= 10;
  } while (x);
  uint32_t len = n + (v < 0);
  if (!out || cap <= len)
    return 0;
  if (v < 0)
    out[k++] = 45;
  while (n)
    out[k++] = d[--n];
  out[k] = 0;
  return k;
}

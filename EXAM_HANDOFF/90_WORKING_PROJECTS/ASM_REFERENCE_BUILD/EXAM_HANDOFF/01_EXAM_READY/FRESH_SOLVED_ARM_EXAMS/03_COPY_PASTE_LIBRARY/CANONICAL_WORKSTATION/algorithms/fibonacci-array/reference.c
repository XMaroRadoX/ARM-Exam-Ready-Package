#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int fibonacci_array(uint32_t *out, uint32_t n, uint32_t cap) {
  if (n > 48 || n > cap || (!out && n))
    return 0;
  for (uint32_t i = 0; i < n; i++)
    out[i] = i < 2 ? i : out[i - 1] + out[i - 2];
  return 1;
}

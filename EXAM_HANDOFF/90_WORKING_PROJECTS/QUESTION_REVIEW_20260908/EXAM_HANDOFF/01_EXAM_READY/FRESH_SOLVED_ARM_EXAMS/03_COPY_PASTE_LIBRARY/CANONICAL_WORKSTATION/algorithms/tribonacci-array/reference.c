#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int tribonacci_array(uint32_t *out, uint32_t n, uint32_t cap) {
  if (n > 32 || n > cap || (!out && n))
    return 0;
  for (uint32_t i = 0; i < n; i++)
    out[i] = i < 2 ? 0 : i == 2 ? 1 : out[i - 1] + out[i - 2] + out[i - 3];
  return 1;
}

#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t bounded_collatz(uint32_t v, uint32_t *out, uint32_t cap) {
  uint32_t n = 0;
  if (!v || !out)
    return 0;
  for (;;) {
    if (n == cap)
      return 0;
    out[n++] = v;
    if (v == 1)
      return n;
    if (v & 1) {
      if (v > 1431655764u)
        return 0;
      v = 3 * v + 1;
    } else
      v /= 2;
  }
}

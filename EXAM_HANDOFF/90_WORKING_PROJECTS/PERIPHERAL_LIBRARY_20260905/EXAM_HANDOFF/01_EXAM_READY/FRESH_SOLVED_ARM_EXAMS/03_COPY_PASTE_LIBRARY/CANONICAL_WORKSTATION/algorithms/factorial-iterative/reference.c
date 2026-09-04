#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int factorial_iterative(uint32_t n, uint32_t *out) {
  if (!out || n > 12)
    return 0;
  uint32_t v = 1;
  while (n)
    v *= n--;
  *out = v;
  return 1;
}

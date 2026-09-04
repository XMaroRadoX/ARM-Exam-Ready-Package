#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int fibonacci_number(uint32_t n, uint32_t *out) {
  if (!out || n > 47)
    return 0;
  if (!n) {
    *out = 0;
    return 1;
  }
  uint32_t a = 0, b = 1;
  while (--n) {
    uint32_t t = a + b;
    a = b;
    b = t;
  }
  *out = b;
  return 1;
}

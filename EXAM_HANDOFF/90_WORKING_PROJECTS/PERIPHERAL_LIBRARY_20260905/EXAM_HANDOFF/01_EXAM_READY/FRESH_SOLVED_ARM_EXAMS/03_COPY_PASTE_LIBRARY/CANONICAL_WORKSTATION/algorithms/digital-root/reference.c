#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t digital_root(uint32_t n) {
  while (n >= 10) {
    uint32_t s = 0;
    do {
      s += n % 10;
      n /= 10;
    } while (n);
    n = s;
  }
  return n;
}

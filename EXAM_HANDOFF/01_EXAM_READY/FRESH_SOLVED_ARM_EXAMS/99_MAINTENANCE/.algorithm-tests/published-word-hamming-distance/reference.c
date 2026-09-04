#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t word_hamming(uint32_t a, uint32_t b) {
  uint32_t x = a ^ b, n = 0;
  while (x) {
    x &= x - 1;
    n++;
  }
  return n;
}

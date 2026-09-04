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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t word_hamming(uint32_t a, uint32_t b);
int test_main(void) {
  CHECK(word_hamming(10, 12) == 2);
  CHECK(word_hamming(0, 0xffffffffu) == 32);
  CHECK(word_hamming(42, 42) == 0);
  return 0;
}

int main(void){return test_main();}

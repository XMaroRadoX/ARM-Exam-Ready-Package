#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t reverse_bits(uint32_t v) {
  uint32_t r = 0;
  for (unsigned i = 0; i < 32; i++) {
    r = (r << 1) | (v & 1);
    v >>= 1;
  }
  return r;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t reverse_bits(uint32_t value);
int test_main(void) {
  CHECK(reverse_bits(13) == 0xb0000000u);
  CHECK(reverse_bits(0) == 0);
  CHECK(reverse_bits(0xffffffffu) == 0xffffffffu);
  CHECK(reverse_bits(reverse_bits(123456)) == 123456);
  return 0;
}

int main(void){return test_main();}

#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t leading_zero_count(uint32_t v) {
  if (!v)
    return 32;
  uint32_t n = 0;
  while (!(v & 0x80000000u)) {
    n++;
    v <<= 1;
  }
  return n;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t leading_zero_count(uint32_t value);
int test_main(void) {
  CHECK(leading_zero_count(8) == 28);
  CHECK(leading_zero_count(0) == 32);
  CHECK(leading_zero_count(0xffffffffu) == 0);
  return 0;
}

int main(void){return test_main();}

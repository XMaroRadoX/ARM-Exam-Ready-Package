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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t digital_root(uint32_t n);
int test_main(void) {
  CHECK(digital_root(9875) == 2);
  CHECK(digital_root(0) == 0);
  CHECK(digital_root(4294967295u) == 3);
  return 0;
}

int main(void){return test_main();}

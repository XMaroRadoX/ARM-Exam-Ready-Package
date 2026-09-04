#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int armstrong_number(uint32_t n) {
  uint32_t k = 0, x = n;
  do {
    k++;
    x /= 10;
  } while (x);
  uint64_t s = 0;
  x = n;
  do {
    uint32_t d = x % 10;
    uint64_t p = 1;
    for (uint32_t i = 0; i < k; i++)
      p *= d;
    s += p;
    x /= 10;
  } while (x);
  return s == n;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int armstrong_number(uint32_t n);
int test_main(void) {
  CHECK(armstrong_number(0));
  CHECK(armstrong_number(153));
  CHECK(armstrong_number(9474));
  CHECK(!armstrong_number(154));
  CHECK(!armstrong_number(4294967295u));
  return 0;
}

int main(void){return test_main();}

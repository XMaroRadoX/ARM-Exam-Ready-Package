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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t bounded_collatz(uint32_t seed, uint32_t *out, uint32_t capacity);
int test_main(void) {
  uint32_t a[10] = {0};
  a[9] = 77;
  CHECK(bounded_collatz(6, a, 9) == 9 && a[8] == 1 && a[9] == 77);
  CHECK(!bounded_collatz(6, a, 2));
  CHECK(bounded_collatz(1, a, 1) == 1);
  CHECK(!bounded_collatz(0, a, 10));
  CHECK(!bounded_collatz(0xffffffffu, a, 10));
  return 0;
}

int main(void){return test_main();}

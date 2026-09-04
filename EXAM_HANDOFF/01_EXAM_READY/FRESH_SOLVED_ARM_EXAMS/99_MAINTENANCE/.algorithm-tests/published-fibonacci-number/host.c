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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int fibonacci_number(uint32_t n, uint32_t *out);
int test_main(void) {
  uint32_t v = 99;
  CHECK(fibonacci_number(0, &v) && v == 0);
  CHECK(fibonacci_number(5, &v) && v == 5);
  CHECK(fibonacci_number(47, &v) && v == 2971215073u);
  CHECK(!fibonacci_number(48, &v) && v == 2971215073u);
  return 0;
}

int main(void){return test_main();}

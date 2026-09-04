#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int fibonacci_array(uint32_t *out, uint32_t n, uint32_t cap) {
  if (n > 48 || n > cap || (!out && n))
    return 0;
  for (uint32_t i = 0; i < n; i++)
    out[i] = i < 2 ? i : out[i - 1] + out[i - 2];
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int fibonacci_array(uint32_t *out, uint32_t count, uint32_t capacity);
int test_main(void) {
  uint32_t a[49] = {0};
  a[48] = 77;
  CHECK(fibonacci_array(a, 7, 7) && a[6] == 8);
  CHECK(!fibonacci_array(a, 8, 7));
  CHECK(fibonacci_array(0, 0, 0));
  CHECK(fibonacci_array(a, 48, 48) && a[48] == 77);
  return 0;
}

int main(void){return test_main();}

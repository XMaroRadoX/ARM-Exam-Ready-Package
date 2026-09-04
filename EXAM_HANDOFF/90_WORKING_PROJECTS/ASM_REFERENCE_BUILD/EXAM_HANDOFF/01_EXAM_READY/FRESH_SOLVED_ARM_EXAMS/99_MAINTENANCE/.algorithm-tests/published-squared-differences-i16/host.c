#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint64_t squared_differences_i16(const int16_t *a, const int16_t *b, uint32_t n) {
  uint64_t s = 0;
  if (a && b)
    for (uint32_t i = 0; i < n; i++) {
      int64_t d = (int32_t)a[i] - b[i];
      s += (uint64_t)(d * d);
    }
  return s;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint64_t squared_differences_i16(const int16_t *a, const int16_t *b, uint32_t n);
int test_main(void) {
  int16_t a[] = {-32768, -32768}, b[] = {32767, 32767};
  CHECK(squared_differences_i16(a, b, 2) == 8589672450ULL);
  CHECK(squared_differences_i16(0, 0, 0) == 0);
  return 0;
}

int main(void){return test_main();}

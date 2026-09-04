#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int64_t dot_i16(const int16_t *a, const int16_t *b, uint32_t n);
int test_main(void) {
  int16_t a[] = {-32768, -32768}, b[] = {-32768, -32768};
  CHECK(dot_i16(a, b, 2) == 2147483648LL);
  CHECK(dot_i16(0, 0, 0) == 0);
  return 0;
}

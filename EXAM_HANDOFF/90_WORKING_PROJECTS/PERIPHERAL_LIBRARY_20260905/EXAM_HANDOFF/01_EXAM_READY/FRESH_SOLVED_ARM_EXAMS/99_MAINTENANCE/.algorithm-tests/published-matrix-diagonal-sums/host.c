#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int diagonal_sums(const int16_t *a, uint32_t n, int64_t *out, uint32_t cap) {
  if (!out || cap < 2 || n > 256 || (!a && n))
    return 0;
  int32_t x = 0, y = 0;
  for (uint32_t i = 0; i < n; i++) {
    x += a[i * n + i];
    y += a[i * n + n - 1 - i];
  }
  out[0] = x;
  out[1] = y;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int diagonal_sums(const int16_t *a, uint32_t n, int64_t *out, uint32_t capacity);
int test_main(void) {
  int16_t a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
  int64_t o[3] = {0};
  o[2] = 77;
  CHECK(diagonal_sums(a, 3, o, 2) && o[0] == 15 && o[1] == 15 && o[2] == 77);
  CHECK(diagonal_sums(0, 0, o, 2) && o[0] == 0);
  CHECK(!diagonal_sums(a, 3, o, 1));
  return 0;
}

int main(void){return test_main();}

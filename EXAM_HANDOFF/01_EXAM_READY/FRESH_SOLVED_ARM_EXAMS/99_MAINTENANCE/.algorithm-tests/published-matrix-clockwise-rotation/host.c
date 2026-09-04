#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_rotate_clockwise(const int32_t *a, uint32_t n, int32_t *out, uint32_t cap) {
  if (n > 256 || cap < n * n || ((!a || !out || a == out) && n))
    return 0;
  for (uint32_t r = 0; r < n; r++)
    for (uint32_t c = 0; c < n; c++)
      out[c * n + n - 1 - r] = a[r * n + c];
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int matrix_rotate_clockwise(const int32_t *a, uint32_t n, int32_t *out,
                            uint32_t capacity);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4}, o[5] = {0};
  o[4] = 77;
  CHECK(matrix_rotate_clockwise(a, 2, o, 4) && o[0] == 3 && o[1] == 1 && o[2] == 4 &&
        o[3] == 2 && o[4] == 77);
  CHECK(!matrix_rotate_clockwise(a, 2, a, 4));
  CHECK(!matrix_rotate_clockwise(a, 2, o, 3));
  return 0;
}

int main(void){return test_main();}

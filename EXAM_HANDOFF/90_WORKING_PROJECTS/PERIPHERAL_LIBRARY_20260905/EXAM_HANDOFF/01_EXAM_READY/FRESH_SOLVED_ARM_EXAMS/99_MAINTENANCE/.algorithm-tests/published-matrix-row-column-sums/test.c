#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_sums(const int16_t *a, uint32_t rows, uint32_t cols, int64_t *out,
                uint32_t capacity);
int test_main(void) {
  int16_t a[] = {1, 2, 3, 4, 5, 6};
  int64_t o[6] = {0};
  o[5] = 77;
  CHECK(matrix_sums(a, 2, 3, o, 5) && o[0] == 6 && o[1] == 15 && o[2] == 5 &&
        o[4] == 9 && o[5] == 77);
  CHECK(!matrix_sums(a, 2, 3, o, 4));
  CHECK(!matrix_sums(a, 0, 3, o, 5));
  return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_transpose(const int *in, size_t rows, size_t cols, int *out);
int test_main(void) {
  int a[] = {1, 2, 3, 4, 5, 6}, o[7] = {0};
  o[6] = 77;
  CHECK(matrix_transpose(a, 2, 3, o) && o[0] == 1 && o[1] == 4 && o[4] == 3 &&
        o[5] == 6 && o[6] == 77);
  CHECK(!matrix_transpose(a, 2, 3, a));
  CHECK(matrix_transpose(0, 0, 4, 0));
  return 0;
}

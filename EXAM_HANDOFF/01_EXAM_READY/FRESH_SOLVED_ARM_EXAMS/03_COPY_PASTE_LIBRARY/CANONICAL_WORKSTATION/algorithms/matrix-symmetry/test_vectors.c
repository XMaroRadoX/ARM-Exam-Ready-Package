#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_symmetric(const int32_t *a, uint32_t n);
int test_main(void) {
  int32_t a[] = {1, 2, 2, 3};
  CHECK(matrix_symmetric(a, 2));
  a[2] = 4;
  CHECK(!matrix_symmetric(a, 2));
  CHECK(matrix_symmetric(0, 0));
  CHECK(!matrix_symmetric(a, 257));
  return 0;
}

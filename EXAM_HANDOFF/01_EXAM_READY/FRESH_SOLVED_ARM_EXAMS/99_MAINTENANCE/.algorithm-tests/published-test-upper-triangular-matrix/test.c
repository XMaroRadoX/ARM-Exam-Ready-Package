#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_is_upper_triangular_i32(const int32_t *matrix, uint32_t size);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 0, 4, 5, 0, 0, 6};
  CHECK(matrix_is_upper_triangular_i32(a, 3));
  a[6] = 9;
  CHECK(!matrix_is_upper_triangular_i32(a, 3));
  CHECK(matrix_is_upper_triangular_i32(0, 0));
  CHECK(!matrix_is_upper_triangular_i32(a, 257));
  return 0;
}

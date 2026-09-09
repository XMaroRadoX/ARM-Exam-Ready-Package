#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_column_maximum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                              uint32_t column_index, int32_t *value_out);
int test_main(void) {
  int32_t a[] = {1, -6, 3, 4, 9, 2}, out = 77;
  CHECK(matrix_column_maximum_i32(a, 2, 3, 1, &out) && out == 9);
  out = 77;
  CHECK(!matrix_column_maximum_i32(a, 2, 3, 3, &out) && out == 77);
  CHECK(!matrix_column_maximum_i32(a, 2, 3, 0, 0));
  return 0;
}

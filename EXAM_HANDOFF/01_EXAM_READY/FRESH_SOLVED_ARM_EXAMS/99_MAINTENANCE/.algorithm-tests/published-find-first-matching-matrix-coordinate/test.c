#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_find_first_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                          int32_t target, uint32_t *row_out, uint32_t *column_out);
int test_main(void) {
  int32_t a[] = {4, 7, 4, 2, 4, 9};
  uint32_t row = 99, column = 99;
  CHECK(matrix_find_first_i32(a, 2, 3, 4, &row, &column) && row == 0 && column == 0);
  row = 99;
  column = 99;
  CHECK(!matrix_find_first_i32(a, 2, 3, 8, &row, &column) && row == 99 && column == 99);
  CHECK(!matrix_find_first_i32(a, 2, 3, 4, &row, &row));
  return 0;
}

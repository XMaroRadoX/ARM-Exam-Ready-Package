#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_border_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                          int64_t *sum_out);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9}, row[] = {1, 2, 3}, column[] = {1, 2, 3};
  int64_t sum = 99;
  CHECK(matrix_border_sum_i32(a, 3, 3, &sum) && sum == 40);
  CHECK(matrix_border_sum_i32(row, 1, 3, &sum) && sum == 6);
  CHECK(matrix_border_sum_i32(column, 3, 1, &sum) && sum == 6);
  CHECK(matrix_border_sum_i32(0, 0, 3, &sum) && sum == 0);
  return 0;
}

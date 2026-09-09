#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_total_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                         int64_t *sum_out);
int test_main(void) {
  int32_t a[] = {1, -2, 3, 4, 5, -6};
  int64_t sum = 99;
  CHECK(matrix_total_sum_i32(a, 2, 3, &sum) && sum == 5);
  CHECK(matrix_total_sum_i32(0, 0, 3, &sum) && sum == 0);
  sum = 99;
  CHECK(!matrix_total_sum_i32(a, 257, 1, &sum) && sum == 99);
  CHECK(!matrix_total_sum_i32(a, 2, 3, 0));
  return 0;
}

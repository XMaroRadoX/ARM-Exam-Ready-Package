#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_swap_columns_i32(int32_t *matrix, uint32_t rows, uint32_t columns,
                            uint32_t first, uint32_t second);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 5, 6};
  CHECK(matrix_swap_columns_i32(a, 2, 3, 0, 2));
  CHECK(a[0] == 3 && a[1] == 2 && a[2] == 1 && a[3] == 6 && a[5] == 4);
  int32_t before = a[0];
  CHECK(!matrix_swap_columns_i32(a, 2, 3, 0, 3) && a[0] == before);
  return 0;
}

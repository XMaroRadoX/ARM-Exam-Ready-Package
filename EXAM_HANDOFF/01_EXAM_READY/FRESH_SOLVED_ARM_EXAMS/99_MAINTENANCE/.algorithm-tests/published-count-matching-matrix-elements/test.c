#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t matrix_count_matches_i32(const int32_t *matrix, uint32_t rows,
                                  uint32_t columns, int32_t target);
int test_main(void) {
  int32_t a[] = {4, 7, 4, 2, 4, 9};
  CHECK(matrix_count_matches_i32(a, 2, 3, 4) == 3);
  CHECK(matrix_count_matches_i32(a, 2, 3, 8) == 0);
  CHECK(matrix_count_matches_i32(0, 0, 3, 4) == 0);
  CHECK(matrix_count_matches_i32(a, 257, 1, 4) == 0);
  return 0;
}

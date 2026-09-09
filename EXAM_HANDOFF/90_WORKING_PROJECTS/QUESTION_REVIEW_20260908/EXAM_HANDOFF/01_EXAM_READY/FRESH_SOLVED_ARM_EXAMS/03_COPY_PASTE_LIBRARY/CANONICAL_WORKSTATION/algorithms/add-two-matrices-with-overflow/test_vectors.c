#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_add_i32(const int32_t *left, const int32_t *right, uint32_t rows,
                   uint32_t columns, int32_t *output, uint32_t capacity);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4}, b[] = {5, 6, 7, 8}, o[5] = {0};
  o[4] = 77;
  CHECK(matrix_add_i32(a, b, 2, 2, o, 4));
  CHECK(o[0] == 6 && o[3] == 12 && o[4] == 77);
  int32_t x[] = {INT32_MAX}, y[] = {1};
  o[0] = 99;
  CHECK(!matrix_add_i32(x, y, 1, 1, o, 1) && o[0] == 99);
  CHECK(!matrix_add_i32(a, b, 2, 2, o, 3));
  return 0;
}

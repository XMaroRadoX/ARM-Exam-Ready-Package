#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Test whether a matrix is an identity matrix
 * Contract: Return 1 when diagonal cells are one and every other cell is zero. size
 * must be at most 256. The empty 0x0 matrix is accepted; a null nonempty matrix is
 * invalid and returns 0. Method:
 * 1. Visit every row and column.
 * 2. Expect one when row equals column.
 * 3. Expect zero everywhere else.
 */
int matrix_is_identity_i32(const int32_t *matrix, uint32_t size) {
  if (size > 256 || (!matrix && size))
    return 0;
  for (uint32_t row = 0; row < size; ++row)
    for (uint32_t column = 0; column < size; ++column)
      if (matrix[row * size + column] != (row == column ? 1 : 0))
        return 0;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int matrix_is_identity_i32(const int32_t *matrix, uint32_t size);
int test_main(void) {
  int32_t a[] = {1, 0, 0, 0, 1, 0, 0, 0, 1};
  CHECK(matrix_is_identity_i32(a, 3));
  a[1] = 2;
  CHECK(!matrix_is_identity_i32(a, 3));
  CHECK(matrix_is_identity_i32(0, 0));
  CHECK(!matrix_is_identity_i32(a, 257));
  return 0;
}

int main(void){return test_main();}

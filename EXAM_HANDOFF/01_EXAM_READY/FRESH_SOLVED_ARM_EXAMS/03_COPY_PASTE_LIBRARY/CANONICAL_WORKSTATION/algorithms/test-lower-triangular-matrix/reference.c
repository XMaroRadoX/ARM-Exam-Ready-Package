#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Test whether a matrix is lower triangular
 * Contract: Return 1 when every cell on the forbidden side of the main diagonal is
 * zero. size must be at most 256. The empty matrix passes; null nonempty input fails.
 * Method:
 * 1. Visit every row and column.
 * 2. Skip the diagonal and allowed side.
 * 3. Reject a nonzero cell on the forbidden side.
 */
int matrix_is_lower_triangular_i32(const int32_t *matrix, uint32_t size) {
  if (size > 256 || (!matrix && size))
    return 0;
  for (uint32_t row = 0; row < size; ++row)
    for (uint32_t column = 0; column < size; ++column)
      if (column > row && matrix[row * size + column] != 0)
        return 0;
  return 1;
}

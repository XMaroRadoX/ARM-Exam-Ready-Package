#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Calculate a matrix border sum
 * Contract: Sum cells in the first or last row or column exactly once. Dimensions must
 * be at most 256. A zero dimension returns zero and permits a null matrix. Method:
 * 1. Handle empty, one-row, and one-column shapes.
 * 2. Sum top and bottom rows.
 * 3. For middle rows, add only first and last cells.
 */
int matrix_border_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                          int64_t *sum_out) {
  if (!sum_out || rows > 256 || columns > 256 || (!matrix && rows && columns))
    return 0;
  int64_t sum = 0;
  for (uint32_t row = 0; row < rows; ++row)
    for (uint32_t column = 0; column < columns; ++column)
      if (row == 0 || row + 1 == rows || column == 0 || column + 1 == columns)
        sum += matrix[row * columns + column];
  *sum_out = sum;
  return 1;
}

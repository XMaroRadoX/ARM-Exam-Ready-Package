#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Find the maximum value in a selected column
 * Contract: Return the signed maximum in one column. Require dimensions 1..256, a valid
 * selected index, and valid pointers. Invalid input writes nothing. Method:
 * 1. Validate the selected column.
 * 2. Seed from its first cell.
 * 3. Advance with the correct contiguous or strided access.
 * 4. Store the final candidate.
 */
int matrix_column_maximum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                              uint32_t column_index, int32_t *value_out) {
  if (!matrix || !value_out || !rows || !columns || rows > 256 || columns > 256 ||
      column_index >= columns)
    return 0;
  int32_t best = matrix[column_index];
  for (uint32_t row = 1; row < rows; ++row)
    if (matrix[row * columns + column_index] > best)
      best = matrix[row * columns + column_index];
  *value_out = best;
  return 1;
}

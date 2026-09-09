#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Swap two matrix columns
 * Contract: Swap two complete columns. Require dimensions 1..256 and both indexes below
 * columns. Equal indexes are a successful no-op. Invalid input writes nothing. Method:
 * 1. Validate dimensions and both columns indexes.
 * 2. Visit each affected cell pair.
 * 3. Load both values before storing the swap.
 */
int matrix_swap_columns_i32(int32_t *matrix, uint32_t rows, uint32_t columns,
                            uint32_t first, uint32_t second) {
  if (!matrix || !rows || !columns || rows > 256 || columns > 256 || first >= columns ||
      second >= columns)
    return 0;
  for (uint32_t row = 0; row < rows; ++row) {
    uint32_t a = row * columns + first, b = row * columns + second;
    int32_t temporary = matrix[a];
    matrix[a] = matrix[b];
    matrix[b] = temporary;
  }
  return 1;
}

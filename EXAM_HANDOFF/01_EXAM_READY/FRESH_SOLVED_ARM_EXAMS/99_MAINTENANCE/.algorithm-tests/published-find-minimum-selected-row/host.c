#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Find the minimum value in a selected row
 * Contract: Return the signed minimum in one row. Require dimensions 1..256, a valid
 * selected index, and valid pointers. Invalid input writes nothing. Method:
 * 1. Validate the selected row.
 * 2. Seed from its first cell.
 * 3. Advance with the correct contiguous or strided access.
 * 4. Store the final candidate.
 */
int matrix_row_minimum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                           uint32_t row_index, int32_t *value_out) {
  if (!matrix || !value_out || !rows || !columns || rows > 256 || columns > 256 ||
      row_index >= rows)
    return 0;
  uint32_t base = row_index * columns;
  int32_t best = matrix[base];
  for (uint32_t column = 1; column < columns; ++column)
    if (matrix[base + column] < best)
      best = matrix[base + column];
  *value_out = best;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int matrix_row_minimum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                           uint32_t row_index, int32_t *value_out);
int test_main(void) {
  int32_t a[] = {1, -6, 3, 4, 9, 2}, out = 77;
  CHECK(matrix_row_minimum_i32(a, 2, 3, 1, &out) && out == 2);
  out = 77;
  CHECK(!matrix_row_minimum_i32(a, 2, 3, 3, &out) && out == 77);
  CHECK(!matrix_row_minimum_i32(a, 2, 3, 0, 0));
  return 0;
}

int main(void){return test_main();}

#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Find the maximum matrix value
 * Contract: Return the signed matrix extremum. Require dimensions 1..256 and valid
 * pointers. Invalid or empty input returns 0 without writing. Method:
 * 1. Validate nonempty dimensions.
 * 2. Seed from the first cell.
 * 3. Scan remaining row-major cells using signed comparisons.
 */
int matrix_maximum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                       int32_t *value_out) {
  if (!matrix || !value_out || !rows || !columns || rows > 256 || columns > 256)
    return 0;
  uint32_t count = rows * columns;
  int32_t best = matrix[0];
  for (uint32_t i = 1; i < count; ++i)
    if (matrix[i] > best)
      best = matrix[i];
  *value_out = best;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int matrix_maximum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                       int32_t *value_out);
int test_main(void) {
  int32_t a[] = {1, -6, 3, 4, 9, 2}, out = 77;
  CHECK(matrix_maximum_i32(a, 2, 3, &out) && out == 9);
  out = 77;
  CHECK(!matrix_maximum_i32(a, 0, 3, &out) && out == 77);
  CHECK(!matrix_maximum_i32(a, 2, 3, 0));
  return 0;
}

int main(void){return test_main();}

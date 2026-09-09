#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Swap two matrix rows
 * Contract: Swap two complete rows. Require dimensions 1..256 and both indexes below
 * rows. Equal indexes are a successful no-op. Invalid input writes nothing. Method:
 * 1. Validate dimensions and both rows indexes.
 * 2. Visit each affected cell pair.
 * 3. Load both values before storing the swap.
 */
int matrix_swap_rows_i32(int32_t *matrix, uint32_t rows, uint32_t columns,
                         uint32_t first, uint32_t second) {
  if (!matrix || !rows || !columns || rows > 256 || columns > 256 || first >= rows ||
      second >= rows)
    return 0;
  for (uint32_t column = 0; column < columns; ++column) {
    uint32_t a = first * columns + column, b = second * columns + column;
    int32_t temporary = matrix[a];
    matrix[a] = matrix[b];
    matrix[b] = temporary;
  }
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int matrix_swap_rows_i32(int32_t *matrix, uint32_t rows, uint32_t columns,
                         uint32_t first, uint32_t second);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 5, 6};
  CHECK(matrix_swap_rows_i32(a, 2, 3, 0, 1));
  CHECK(a[0] == 4 && a[1] == 5 && a[2] == 6 && a[3] == 1 && a[5] == 3);
  int32_t before = a[0];
  CHECK(!matrix_swap_rows_i32(a, 2, 3, 0, 3) && a[0] == before);
  return 0;
}

int main(void){return test_main();}

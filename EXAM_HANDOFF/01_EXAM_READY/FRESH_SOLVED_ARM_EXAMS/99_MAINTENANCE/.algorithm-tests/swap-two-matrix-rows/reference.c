#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Swap two matrix rows
 * Contract: Swap two complete rows. Require dimensions 1..256 and both indexes below rows. Equal indexes are a successful no-op. Invalid input writes nothing.
 * Method:
 * 1. Validate dimensions and both rows indexes.
 * 2. Visit each affected cell pair.
 * 3. Load both values before storing the swap.
 */
int matrix_swap_rows_i32(int32_t *matrix, uint32_t rows, uint32_t columns,
                      uint32_t first, uint32_t second) {
  if(!matrix || !rows || !columns || rows>256 || columns>256 ||
     first>=rows || second>=rows) return 0;
  for(uint32_t column=0;column<columns;++column) {
    uint32_t a=first*columns+column, b=second*columns+column;
    int32_t temporary=matrix[a];matrix[a]=matrix[b];matrix[b]=temporary;
  }
  return 1;
}

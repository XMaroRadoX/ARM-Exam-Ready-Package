#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Find the first matching matrix coordinate
 * Contract: Find the first row-major cell equal to target. Require dimensions 1..256 and distinct valid output pointers. Failure or invalid input leaves both outputs unchanged.
 * Method:
 * 1. Validate every pointer and dimension.
 * 2. Scan flat indexes from zero.
 * 3. Divide the first matching index by columns to recover row and remainder column.
 */
int matrix_find_first_i32(const int32_t *matrix, uint32_t rows,
                          uint32_t columns, int32_t target,
                          uint32_t *row_out, uint32_t *column_out) {
  if(!matrix || !row_out || !column_out || row_out==column_out ||
     !rows || !columns || rows>256 || columns>256) return 0;
  uint32_t count=rows*columns;
  for(uint32_t i=0;i<count;++i) if(matrix[i]==target) {
    *row_out=i/columns; *column_out=i%columns; return 1;
  }
  return 0;
}

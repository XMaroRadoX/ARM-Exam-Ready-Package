#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Count matching matrix elements
 * Contract: Count cells equal to target in a matrix with dimensions at most 256. A zero dimension returns zero and permits a null matrix pointer. Other invalid input returns zero.
 * Method:
 * 1. Validate dimensions.
 * 2. Convert dimensions to a bounded flat count.
 * 3. Scan and increment for exact signed equality.
 */
uint32_t matrix_count_matches_i32(const int32_t *matrix, uint32_t rows,
                                  uint32_t columns, int32_t target) {
  if(rows>256 || columns>256 || (!matrix && rows && columns)) return 0;
  uint32_t matches=0;
  for(uint32_t i=0;i<rows*columns;++i) if(matrix[i]==target) ++matches;
  return matches;
}

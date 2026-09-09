#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Subtract two matrices with overflow detection
 * Contract: Perform elementwise signed int32_t arithmetic. Require dimensions at most 256, enough disjoint output storage, and no cell overflow. A complete preflight guarantees failure performs no writes.
 * Method:
 * 1. Validate dimensions, capacity, and pointers.
 * 2. Preflight every cell using widened arithmetic.
 * 3. Repeat the scan and store only after all cells are safe.
 */
int matrix_subtract_i32(const int32_t *left, const int32_t *right,
                      uint32_t rows, uint32_t columns,
                      int32_t *output, uint32_t capacity) {
  if(rows>256 || columns>256) return 0;
  uint32_t count=rows*columns;
  if(capacity<count || ((!left||!right||!output)&&count)) return 0;
  for(uint32_t i=0;i<count;++i) {
    int64_t wide=(int64_t)left[i]-right[i];
    if(wide<INT32_MIN || wide>INT32_MAX) return 0;
  }
  for(uint32_t i=0;i<count;++i) output[i]=left[i]-right[i];
  return 1;
}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Test whether a matrix is upper triangular
 * Contract: Return 1 when every cell on the forbidden side of the main diagonal is zero. size must be at most 256. The empty matrix passes; null nonempty input fails.
 * Method:
 * 1. Visit every row and column.
 * 2. Skip the diagonal and allowed side.
 * 3. Reject a nonzero cell on the forbidden side.
 */
int matrix_is_upper_triangular_i32(const int32_t *matrix, uint32_t size) {
  if(size>256 || (!matrix&&size)) return 0;
  for(uint32_t row=0;row<size;++row)
    for(uint32_t column=0;column<size;++column)
      if(row>column && matrix[row*size+column]!=0) return 0;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int matrix_is_upper_triangular_i32(const int32_t *matrix, uint32_t size);
int test_main(void) {
int32_t a[]={1,2,3,0,4,5,0,0,6};
CHECK(matrix_is_upper_triangular_i32(a,3));a[6]=9;CHECK(!matrix_is_upper_triangular_i32(a,3));
CHECK(matrix_is_upper_triangular_i32(0,0));CHECK(!matrix_is_upper_triangular_i32(a,257));
return 0;
}

int main(void){return test_main();}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Sum all matrix elements
 * Contract: Sum a contiguous row-major int32_t matrix into int64_t. rows and columns must each be at most 256. A zero dimension produces zero and permits a null matrix pointer. Invalid input returns 0 without writing.
 * Method:
 * 1. Validate dimensions and output.
 * 2. Multiply rows by columns after applying the bounds.
 * 3. Sign-extend and accumulate each cell.
 * 4. Publish the final sum.
 */
int matrix_total_sum_i32(const int32_t *matrix, uint32_t rows,
                         uint32_t columns, int64_t *sum_out) {
  if(!sum_out || rows>256 || columns>256 ||
     (!matrix && rows && columns)) return 0;
  int64_t sum=0;
  for(uint32_t i=0;i<rows*columns;++i) sum+=matrix[i];
  *sum_out=sum;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int matrix_total_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int64_t *sum_out);
int test_main(void) {
int32_t a[]={1,-2,3,4,5,-6};int64_t sum=99;
CHECK(matrix_total_sum_i32(a,2,3,&sum)&&sum==5);
CHECK(matrix_total_sum_i32(0,0,3,&sum)&&sum==0);
sum=99;CHECK(!matrix_total_sum_i32(a,257,1,&sum)&&sum==99);
CHECK(!matrix_total_sum_i32(a,2,3,0));
return 0;
}

int main(void){return test_main();}

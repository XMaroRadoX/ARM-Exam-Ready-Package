#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Calculate a square matrix trace
 * Contract: Sum the main diagonal of a contiguous square int32_t matrix. size must be at most 256. A 0x0 matrix has trace zero and may be null.
 * Method:
 * 1. Validate size and pointers.
 * 2. Start at index zero.
 * 3. Advance by size+1 to visit each diagonal cell.
 * 4. Accumulate in 64 bits.
 */
int matrix_trace_i32(const int32_t *matrix, uint32_t size,
                     int64_t *trace_out) {
  if(!trace_out || size>256 || (!matrix && size)) return 0;
  int64_t trace=0;
  for(uint32_t i=0;i<size;++i) trace+=matrix[i*size+i];
  *trace_out=trace;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int matrix_trace_i32(const int32_t *matrix, uint32_t size, int64_t *trace_out);
int test_main(void) {
int32_t a[]={1,2,3,4,5,6,7,8,9};int64_t trace=99;
CHECK(matrix_trace_i32(a,3,&trace)&&trace==15);
CHECK(matrix_trace_i32(0,0,&trace)&&trace==0);
trace=99;CHECK(!matrix_trace_i32(a,257,&trace)&&trace==99);
return 0;
}

int main(void){return test_main();}

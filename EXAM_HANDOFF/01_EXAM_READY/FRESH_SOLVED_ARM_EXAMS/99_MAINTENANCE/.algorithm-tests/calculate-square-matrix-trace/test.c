#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
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

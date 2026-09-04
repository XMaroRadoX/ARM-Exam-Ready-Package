#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_multiply_i16(const int16_t *a, const int16_t *b, uint32_t rows, uint32_t inner, uint32_t cols, int64_t *out, uint32_t capacity);
int test_main(void) {
int16_t a[]={1,2,3,4},b[]={5,6,7,8};int64_t o[5]={0};o[4]=77;CHECK(matrix_multiply_i16(a,b,2,2,2,o,4)&&o[0]==19&&o[1]==22&&o[2]==43&&o[3]==50&&o[4]==77);CHECK(!matrix_multiply_i16(a,b,2,2,2,o,3));int16_t x[]={-32768,-32768};CHECK(matrix_multiply_i16(x,x,1,2,1,o,1)&&o[0]==2147483648LL);
return 0;
}

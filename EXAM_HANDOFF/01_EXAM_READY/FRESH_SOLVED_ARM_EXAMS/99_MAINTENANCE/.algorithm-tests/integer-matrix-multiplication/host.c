#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_multiply_i16(const int16_t*a,const int16_t*b,uint32_t r,uint32_t k,uint32_t c,int64_t*out,uint32_t cap){if(!a||!b||!out||!r||!k||!c||r>256||k>256||c>256||cap<r*c)return 0;for(uint32_t i=0;i<r;i++)for(uint32_t j=0;j<c;j++){int64_t s=0;for(uint32_t t=0;t<k;t++)s+=(int32_t)a[i*k+t]*b[t*c+j];out[i*c+j]=s;}return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int matrix_multiply_i16(const int16_t *a, const int16_t *b, uint32_t rows, uint32_t inner, uint32_t cols, int64_t *out, uint32_t capacity);
int test_main(void) {
int16_t a[]={1,2,3,4},b[]={5,6,7,8};int64_t o[5]={0};o[4]=77;CHECK(matrix_multiply_i16(a,b,2,2,2,o,4)&&o[0]==19&&o[1]==22&&o[2]==43&&o[3]==50&&o[4]==77);CHECK(!matrix_multiply_i16(a,b,2,2,2,o,3));int16_t x[]={-32768,-32768};CHECK(matrix_multiply_i16(x,x,1,2,1,o,1)&&o[0]==2147483648LL);
return 0;
}

int main(void){return test_main();}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_sums(const int16_t*a,uint32_t r,uint32_t c,int64_t*out,uint32_t cap){if(!a||!out||!r||!c||r>256||c>256||cap<r+c)return 0;for(uint32_t i=0;i<r;i++){int32_t s=0;for(uint32_t j=0;j<c;j++)s+=a[i*c+j];out[i]=s;}for(uint32_t j=0;j<c;j++){int32_t s=0;for(uint32_t i=0;i<r;i++)s+=a[i*c+j];out[r+j]=s;}return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int matrix_sums(const int16_t *a, uint32_t rows, uint32_t cols, int64_t *out, uint32_t capacity);
int test_main(void) {
int16_t a[]={1,2,3,4,5,6};int64_t o[6]={0};o[5]=77;CHECK(matrix_sums(a,2,3,o,5)&&o[0]==6&&o[1]==15&&o[2]==5&&o[4]==9&&o[5]==77);CHECK(!matrix_sums(a,2,3,o,4));CHECK(!matrix_sums(a,0,3,o,5));
return 0;
}

int main(void){return test_main();}

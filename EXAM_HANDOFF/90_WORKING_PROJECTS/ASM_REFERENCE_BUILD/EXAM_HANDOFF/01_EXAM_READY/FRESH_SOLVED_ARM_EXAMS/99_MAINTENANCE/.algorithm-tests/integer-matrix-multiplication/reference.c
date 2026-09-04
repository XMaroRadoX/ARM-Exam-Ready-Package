#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_multiply_i16(const int16_t*a,const int16_t*b,uint32_t r,uint32_t k,uint32_t c,int64_t*out,uint32_t cap){if(!a||!b||!out||!r||!k||!c||r>256||k>256||c>256||cap<r*c)return 0;for(uint32_t i=0;i<r;i++)for(uint32_t j=0;j<c;j++){int64_t s=0;for(uint32_t t=0;t<k;t++)s+=(int32_t)a[i*k+t]*b[t*c+j];out[i*c+j]=s;}return 1;}

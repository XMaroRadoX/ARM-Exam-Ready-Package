#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int64_t dot_i16(const int16_t*a,const int16_t*b,uint32_t n){int64_t s=0;if(a&&b)for(uint32_t i=0;i<n;i++){s+=(int64_t)a[i]*b[i];}return s;}

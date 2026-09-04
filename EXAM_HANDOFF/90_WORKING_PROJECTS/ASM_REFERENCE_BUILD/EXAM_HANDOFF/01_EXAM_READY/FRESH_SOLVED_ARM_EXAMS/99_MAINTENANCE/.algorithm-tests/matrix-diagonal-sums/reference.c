#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int diagonal_sums(const int16_t*a,uint32_t n,int64_t*out,uint32_t cap){if(!out||cap<2||n>256||(!a&&n))return 0;int32_t x=0,y=0;for(uint32_t i=0;i<n;i++){x+=a[i*n+i];y+=a[i*n+n-1-i];}out[0]=x;out[1]=y;return 1;}

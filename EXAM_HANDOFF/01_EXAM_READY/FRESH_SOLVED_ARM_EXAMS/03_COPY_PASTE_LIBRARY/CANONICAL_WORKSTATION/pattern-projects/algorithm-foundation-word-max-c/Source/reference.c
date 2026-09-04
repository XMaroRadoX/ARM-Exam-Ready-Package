#include <stdint.h>
uint32_t array_max_u32(const uint32_t*a,uint32_t n){uint32_t x=a[0],i;for(i=1;i<n;i++)if(a[i]>x)x=a[i];return x;}
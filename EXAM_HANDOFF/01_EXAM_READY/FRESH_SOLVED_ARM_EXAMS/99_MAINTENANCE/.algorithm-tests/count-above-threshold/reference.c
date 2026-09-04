#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t count_above(const int32_t*a,uint32_t n,int32_t t){uint32_t c=0;if(a)for(uint32_t i=0;i<n;i++)if(a[i]>t)c++;return c;}

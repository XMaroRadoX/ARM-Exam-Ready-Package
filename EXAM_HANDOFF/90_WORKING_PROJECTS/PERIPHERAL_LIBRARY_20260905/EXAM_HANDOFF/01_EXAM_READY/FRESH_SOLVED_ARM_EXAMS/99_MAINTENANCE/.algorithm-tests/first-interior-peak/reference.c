#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int32_t first_peak(const int32_t*a,uint32_t n){if(!a||n<3||n>INT32_MAX)return -1;for(uint32_t i=1;i+1<n;i++)if(a[i]>a[i-1]&&a[i]>a[i+1])return (int32_t)i;return -1;}

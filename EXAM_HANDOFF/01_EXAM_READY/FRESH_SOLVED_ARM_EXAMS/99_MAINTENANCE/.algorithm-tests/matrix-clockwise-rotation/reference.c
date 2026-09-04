#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_rotate_clockwise(const int32_t*a,uint32_t n,int32_t*out,uint32_t cap){if(n>256||cap<n*n||((!a||!out||a==out)&&n))return 0;for(uint32_t r=0;r<n;r++)for(uint32_t c=0;c<n;c++)out[c*n+n-1-r]=a[r*n+c];return 1;}

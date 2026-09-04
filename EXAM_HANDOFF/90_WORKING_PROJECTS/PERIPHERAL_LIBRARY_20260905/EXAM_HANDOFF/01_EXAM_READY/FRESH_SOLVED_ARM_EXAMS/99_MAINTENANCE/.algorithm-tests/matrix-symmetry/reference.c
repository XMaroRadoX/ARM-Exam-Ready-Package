#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_symmetric(const int32_t*a,uint32_t n){if(n>256||(!a&&n))return 0;for(uint32_t r=0;r<n;r++)for(uint32_t c=r+1;c<n;c++)if(a[r*n+c]!=a[c*n+r])return 0;return 1;}

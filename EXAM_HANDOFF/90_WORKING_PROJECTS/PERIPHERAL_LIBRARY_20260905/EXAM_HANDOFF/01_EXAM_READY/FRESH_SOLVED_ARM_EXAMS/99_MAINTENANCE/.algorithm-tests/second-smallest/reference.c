#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int second_smallest(const int32_t*a,uint32_t n,int32_t*out){if(!a||!out||!n)return 0;int32_t best=a[0],second=0;int have=0;for(uint32_t i=1;i<n;i++){int32_t x=a[i];if(x<best){second=best;best=x;have=1;}else if(x!=best&&(!have||x<second)){second=x;have=1;}}if(have)*out=second;return have;}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int64_t maximum_subarray(const int32_t*a,uint32_t n){if(!a||!n)return 0;int64_t cur=a[0],best=cur;for(uint32_t i=1;i<n;i++){if(cur<0)cur=0;cur+=a[i];if(cur>best)best=cur;}return best;}

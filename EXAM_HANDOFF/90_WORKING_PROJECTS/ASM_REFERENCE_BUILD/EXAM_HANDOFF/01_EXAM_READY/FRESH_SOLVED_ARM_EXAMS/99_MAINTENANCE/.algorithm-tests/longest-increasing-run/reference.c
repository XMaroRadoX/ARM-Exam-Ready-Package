#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t longest_increasing_run(const int32_t*a,uint32_t n){if(!a||!n)return 0;uint32_t r=1,b=1;for(uint32_t i=1;i<n;i++){r=a[i]>a[i-1]?r+1:1;if(r>b)b=r;}return b;}

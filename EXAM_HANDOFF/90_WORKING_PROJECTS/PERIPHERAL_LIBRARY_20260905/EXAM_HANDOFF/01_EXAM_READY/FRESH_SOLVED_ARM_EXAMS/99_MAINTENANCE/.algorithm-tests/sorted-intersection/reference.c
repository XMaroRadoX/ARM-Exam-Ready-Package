#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t sorted_intersection(const int32_t*a,uint32_t n,const int32_t*b,uint32_t m,int32_t*out,uint32_t cap){if(n>UINT32_MAX-m||cap<n+m||(!a&&n)||(!b&&m)||(!out&&(n||m)))return UINT32_MAX;uint32_t i=0,j=0,k=0;while(i<n&&j<m){if(a[i]<b[j])i++;else if(a[i]>b[j])j++;else{int32_t x=a[i++];j++;if(!k||out[k-1]!=x)out[k++]=x;}}return k;}

#include <stdint.h>
int first_equal_pair(const uint32_t*a,const uint32_t*b,uint32_t n,uint32_t m){uint32_t i,j;for(i=0;i<n;i++)for(j=0;j<m;j++)if(a[i]==b[j])return (int)((i<<16)|j);return -1;}
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int32_t substring_first(const uint8_t*s,uint32_t n,const uint8_t*p,uint32_t m){if(n>INT32_MAX||(!s&&n)||(!p&&m))return -1;if(!m)return 0;if(m>n)return -1;uint32_t k=0;(void)k;for(uint32_t i=0;i<=n-m;i++){uint32_t j=0;while(j<m&&s[i+j]==p[j])j++;if(j==m){return (int32_t)i;}}return -1;}

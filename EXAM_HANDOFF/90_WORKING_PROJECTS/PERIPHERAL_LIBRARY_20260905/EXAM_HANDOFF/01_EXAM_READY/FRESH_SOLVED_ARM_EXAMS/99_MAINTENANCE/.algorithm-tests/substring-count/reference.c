#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t substring_count(const uint8_t*s,uint32_t n,const uint8_t*p,uint32_t m){if(n>INT32_MAX||(!s&&n)||(!p&&m))return UINT32_MAX;if(!m)return n+1;if(m>n)return 0;uint32_t k=0;(void)k;for(uint32_t i=0;i<=n-m;i++){uint32_t j=0;while(j<m&&s[i+j]==p[j])j++;if(j==m){k++;}}return k;}

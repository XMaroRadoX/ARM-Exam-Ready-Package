#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int binomial_coefficient(uint32_t n,uint32_t k,uint32_t*out){if(!out||n>30||k>n)return 0;if(k>n-k)k=n-k;uint32_t v=1;for(uint32_t i=1;i<=k;i++)v=v*(n-k+i)/i;*out=v;return 1;}

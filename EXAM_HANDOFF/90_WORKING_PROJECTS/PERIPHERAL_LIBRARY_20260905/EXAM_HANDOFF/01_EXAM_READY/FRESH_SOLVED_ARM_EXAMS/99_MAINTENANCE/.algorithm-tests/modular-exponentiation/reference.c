#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int modular_power(uint32_t b,uint32_t e,uint32_t m,uint32_t*out){if(!out||!m||m>65535)return 0;b%=m;uint32_t r=1%m;while(e){if(e&1)r=(r*b)%m;e>>=1;b=(b*b)%m;}*out=r;return 1;}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int reverse_decimal(uint32_t n,uint32_t*out){if(!out)return 0;uint64_t v=0;do{v=v*10+n%10;if(v>UINT32_MAX)return 0;n/=10;}while(n);*out=(uint32_t)v;return 1;}

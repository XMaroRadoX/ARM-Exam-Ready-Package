#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int packed_bcd(uint32_t v,uint32_t*out){if(!out||v>99999999)return 0;uint32_t r=0;for(uint32_t i=0;i<8;i++){r|=(v%10)<<(4*i);v/=10;}*out=r;return 1;}

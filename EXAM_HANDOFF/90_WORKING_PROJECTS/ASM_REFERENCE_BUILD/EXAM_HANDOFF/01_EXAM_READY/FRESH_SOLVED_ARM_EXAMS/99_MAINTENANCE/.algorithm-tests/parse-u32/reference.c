#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int parse_u32(const uint8_t*s,uint32_t n,uint32_t*out){if(!s||!out||!n)return 0;uint32_t v=0;for(uint32_t i=0;i<n;i++){if(s[i]<48||s[i]>57)return 0;uint32_t d=s[i]-48;if(v>429496729u||(v==429496729u&&d>5))return 0;v=v*10+d;}*out=v;return 1;}

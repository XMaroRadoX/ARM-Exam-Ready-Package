#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int parse_i32(const uint8_t*s,uint32_t n,int32_t*out){if(!s||!out||!n)return 0;int neg=0;if(n&&(s[0]==45||s[0]==43)){neg=s[0]==45;s++;n--;}if(!n)return 0;uint32_t v=0;for(uint32_t i=0;i<n;i++){if(s[i]<48||s[i]>57)return 0;uint32_t d=s[i]-48;if(v>429496729u||(v==429496729u&&d>5))return 0;v=v*10+d;}if(v>(neg?2147483648u:2147483647u))return 0;*out=neg?(int32_t)(-(int64_t)v):(int32_t)v;return 1;}

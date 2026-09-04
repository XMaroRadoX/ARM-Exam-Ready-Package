#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int bit_palindrome(uint32_t v,uint32_t w){if(w>32)return 0;uint32_t r=0,x=v;for(uint32_t i=0;i<w;i++){r=(r<<1)|(x&1);x>>=1;}uint32_t m=w==32?UINT32_MAX:w?((1u<<w)-1):0;return r==(v&m);}

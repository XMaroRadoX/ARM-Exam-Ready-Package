#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t reverse_bits(uint32_t v){uint32_t r=0;for(unsigned i=0;i<32;i++){r=(r<<1)|(v&1);v>>=1;}return r;}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
static uint64_t divisor_sum_core(uint32_t n){uint64_t s=0;for(uint32_t d=1;n&&d<=n/d;d++)if(n%d==0){s+=d;if(d!=n/d)s+=n/d;}return s;}int perfect_number(uint32_t n){return n>1&&divisor_sum_core(n)==(uint64_t)n*2;}

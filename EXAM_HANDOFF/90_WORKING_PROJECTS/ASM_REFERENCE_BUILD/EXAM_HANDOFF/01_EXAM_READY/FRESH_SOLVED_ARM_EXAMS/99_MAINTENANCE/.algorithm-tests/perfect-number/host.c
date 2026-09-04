#include <stdint.h>
#include <stddef.h>
#include <limits.h>
static uint64_t divisor_sum_core(uint32_t n){uint64_t s=0;for(uint32_t d=1;n&&d<=n/d;d++)if(n%d==0){s+=d;if(d!=n/d)s+=n/d;}return s;}int perfect_number(uint32_t n){return n>1&&divisor_sum_core(n)==(uint64_t)n*2;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int perfect_number(uint32_t n);
int test_main(void) {
CHECK(perfect_number(6));CHECK(perfect_number(28));CHECK(!perfect_number(1));CHECK(!perfect_number(12));CHECK(!perfect_number(0));
return 0;
}

int main(void){return test_main();}

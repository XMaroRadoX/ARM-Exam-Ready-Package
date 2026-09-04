#include <stdint.h>
#include <stddef.h>
#include <limits.h>
static uint64_t divisor_sum_core(uint32_t n){uint64_t s=0;for(uint32_t d=1;n&&d<=n/d;d++)if(n%d==0){s+=d;if(d!=n/d)s+=n/d;}return s;}uint64_t divisor_sum(uint32_t n){return divisor_sum_core(n);}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint64_t divisor_sum(uint32_t n);
int test_main(void) {
CHECK(divisor_sum(0)==0);CHECK(divisor_sum(1)==1);CHECK(divisor_sum(12)==28);CHECK(divisor_sum(36)==91);
return 0;
}

int main(void){return test_main();}

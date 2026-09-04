#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t divisor_count(uint32_t n){uint32_t c=0;for(uint32_t d=1;n&&d<=n/d;d++)if(n%d==0)c+=d==n/d?1:2;return c;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t divisor_count(uint32_t n);
int test_main(void) {
CHECK(divisor_count(0)==0);CHECK(divisor_count(1)==1);CHECK(divisor_count(36)==9);CHECK(divisor_count(13)==2);
return 0;
}

int main(void){return test_main();}

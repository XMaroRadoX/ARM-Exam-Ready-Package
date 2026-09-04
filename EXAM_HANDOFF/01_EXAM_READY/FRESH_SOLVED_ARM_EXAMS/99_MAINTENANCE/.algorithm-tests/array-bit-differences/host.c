#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint64_t array_bit_differences(const uint32_t*a,const uint32_t*b,uint32_t n){uint64_t s=0;if(a&&b)for(uint32_t i=0;i<n;i++){uint32_t x=a[i]^b[i];while(x){s++;x&=x-1;}}return s;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint64_t array_bit_differences(const uint32_t *a, const uint32_t *b, uint32_t n);
int test_main(void) {
uint32_t a[]={0,0xffffffffu},b[]={0xffffffffu,0};CHECK(array_bit_differences(a,b,2)==64);CHECK(array_bit_differences(0,0,0)==0);
return 0;
}

int main(void){return test_main();}

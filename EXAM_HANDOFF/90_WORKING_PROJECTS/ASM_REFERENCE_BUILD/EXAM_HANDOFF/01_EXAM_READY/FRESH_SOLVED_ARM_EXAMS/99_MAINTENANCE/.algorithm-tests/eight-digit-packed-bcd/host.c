#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int packed_bcd(uint32_t v,uint32_t*out){if(!out||v>99999999)return 0;uint32_t r=0;for(uint32_t i=0;i<8;i++){r|=(v%10)<<(4*i);v/=10;}*out=r;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int packed_bcd(uint32_t value, uint32_t *out);
int test_main(void) {
uint32_t v=0;CHECK(packed_bcd(12345678,&v)&&v==0x12345678);CHECK(packed_bcd(42,&v)&&v==0x42);CHECK(packed_bcd(0,&v)&&v==0);v=99;CHECK(!packed_bcd(100000000,&v)&&v==99);
return 0;
}

int main(void){return test_main();}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int modular_power(uint32_t b,uint32_t e,uint32_t m,uint32_t*out){if(!out||!m||m>65535)return 0;b%=m;uint32_t r=1%m;while(e){if(e&1)r=(r*b)%m;e>>=1;b=(b*b)%m;}*out=r;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int modular_power(uint32_t base, uint32_t exponent, uint32_t modulus, uint32_t *out);
int test_main(void) {
uint32_t v=9;CHECK(modular_power(3,5,7,&v)&&v==5);CHECK(modular_power(2,0,1,&v)&&v==0);CHECK(!modular_power(3,2,0,&v));CHECK(modular_power(65534,2,65535,&v)&&v==1);
return 0;
}

int main(void){return test_main();}

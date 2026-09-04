#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int parse_u32(const uint8_t*s,uint32_t n,uint32_t*out){if(!s||!out||!n)return 0;uint32_t v=0;for(uint32_t i=0;i<n;i++){if(s[i]<48||s[i]>57)return 0;uint32_t d=s[i]-48;if(v>429496729u||(v==429496729u&&d>5))return 0;v=v*10+d;}*out=v;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int parse_u32(const uint8_t *text, uint32_t length, uint32_t *out);
int test_main(void) {
uint32_t v=99;CHECK(parse_u32((const uint8_t*)"123",3,&v)&&v==123);v=99;CHECK(!parse_u32((const uint8_t*)"12x",3,&v)&&v==99);CHECK(!parse_u32((const uint8_t*)"",0,&v));CHECK(parse_u32((const uint8_t*)"4294967295",10,&v)&&v==UINT32_MAX);CHECK(!parse_u32((const uint8_t*)"4294967296",10,&v));
return 0;
}

int main(void){return test_main();}

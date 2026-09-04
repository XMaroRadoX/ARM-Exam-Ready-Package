#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t trailing_zero_count(uint32_t v){if(!v)return 32;uint32_t n=0;while(!(v&1u)){n++;v>>=1;}return n;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t trailing_zero_count(uint32_t value);
int test_main(void) {
{
CHECK(trailing_zero_count(0u)==32u);
CHECK(trailing_zero_count(1u)==0u);
CHECK(trailing_zero_count(2u)==1u);
CHECK(trailing_zero_count(9u)==0u);
CHECK(trailing_zero_count(10u)==1u);
CHECK(trailing_zero_count(123321u)==0u);
CHECK(trailing_zero_count(4000000004u)==2u);
CHECK(trailing_zero_count(4294967295u)==0u);
CHECK(trailing_zero_count(264951055u)==0u);
CHECK(trailing_zero_count(3302568628u)==2u);
CHECK(trailing_zero_count(1461547428u)==2u);
CHECK(trailing_zero_count(4165108330u)==1u);
CHECK(trailing_zero_count(999144594u)==1u);
CHECK(trailing_zero_count(4017729701u)==0u);
CHECK(trailing_zero_count(969213969u)==0u);
CHECK(trailing_zero_count(3989968933u)==0u);
CHECK(trailing_zero_count(1681659299u)==0u);
CHECK(trailing_zero_count(1137519360u)==8u);
CHECK(trailing_zero_count(1940529389u)==0u);
CHECK(trailing_zero_count(3538678198u)==1u);
CHECK(trailing_zero_count(3395160109u)==0u);
CHECK(trailing_zero_count(924203215u)==0u);
CHECK(trailing_zero_count(3951801352u)==3u);
CHECK(trailing_zero_count(3065865433u)==0u);
CHECK(trailing_zero_count(2864782762u)==1u);
CHECK(trailing_zero_count(1356993055u)==0u);
CHECK(trailing_zero_count(703953597u)==0u);
CHECK(trailing_zero_count(361964270u)==1u);
CHECK(trailing_zero_count(1958511902u)==1u);
CHECK(trailing_zero_count(1968465316u)==2u);
CHECK(trailing_zero_count(3810760418u)==1u);
CHECK(trailing_zero_count(3773631281u)==0u);
}

CHECK(trailing_zero_count(8)==3);CHECK(trailing_zero_count(0)==32);CHECK(trailing_zero_count(0xffffffffu)==0);
return 0;
}

int main(void){return test_main();}

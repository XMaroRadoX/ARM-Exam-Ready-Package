#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t leading_zero_count(uint32_t value);
int test_main(void) {
{
CHECK(leading_zero_count(0u)==32u);
CHECK(leading_zero_count(1u)==31u);
CHECK(leading_zero_count(2u)==30u);
CHECK(leading_zero_count(9u)==28u);
CHECK(leading_zero_count(10u)==28u);
CHECK(leading_zero_count(123321u)==15u);
CHECK(leading_zero_count(4000000004u)==0u);
CHECK(leading_zero_count(4294967295u)==0u);
CHECK(leading_zero_count(264951055u)==4u);
CHECK(leading_zero_count(3302568628u)==0u);
CHECK(leading_zero_count(1461547428u)==1u);
CHECK(leading_zero_count(4165108330u)==0u);
CHECK(leading_zero_count(999144594u)==2u);
CHECK(leading_zero_count(4017729701u)==0u);
CHECK(leading_zero_count(969213969u)==2u);
CHECK(leading_zero_count(3989968933u)==0u);
CHECK(leading_zero_count(1681659299u)==1u);
CHECK(leading_zero_count(1137519360u)==1u);
CHECK(leading_zero_count(1940529389u)==1u);
CHECK(leading_zero_count(3538678198u)==0u);
CHECK(leading_zero_count(3395160109u)==0u);
CHECK(leading_zero_count(924203215u)==2u);
CHECK(leading_zero_count(3951801352u)==0u);
CHECK(leading_zero_count(3065865433u)==0u);
CHECK(leading_zero_count(2864782762u)==0u);
CHECK(leading_zero_count(1356993055u)==1u);
CHECK(leading_zero_count(703953597u)==2u);
CHECK(leading_zero_count(361964270u)==3u);
CHECK(leading_zero_count(1958511902u)==1u);
CHECK(leading_zero_count(1968465316u)==1u);
CHECK(leading_zero_count(3810760418u)==0u);
CHECK(leading_zero_count(3773631281u)==0u);
}

CHECK(leading_zero_count(8)==28);CHECK(leading_zero_count(0)==32);CHECK(leading_zero_count(0xffffffffu)==0);
return 0;
}

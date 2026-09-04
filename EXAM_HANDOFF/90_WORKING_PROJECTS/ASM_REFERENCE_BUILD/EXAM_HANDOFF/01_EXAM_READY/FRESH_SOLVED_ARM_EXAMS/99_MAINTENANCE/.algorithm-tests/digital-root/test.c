#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t digital_root(uint32_t n);
int test_main(void) {
{
CHECK(digital_root(0u)==0u);
CHECK(digital_root(1u)==1u);
CHECK(digital_root(2u)==2u);
CHECK(digital_root(9u)==9u);
CHECK(digital_root(10u)==1u);
CHECK(digital_root(123321u)==3u);
CHECK(digital_root(4000000004u)==8u);
CHECK(digital_root(4294967295u)==3u);
CHECK(digital_root(264951055u)==1u);
CHECK(digital_root(3302568628u)==7u);
CHECK(digital_root(1461547428u)==6u);
CHECK(digital_root(4165108330u)==4u);
CHECK(digital_root(999144594u)==9u);
CHECK(digital_root(4017729701u)==2u);
CHECK(digital_root(969213969u)==9u);
CHECK(digital_root(3989968933u)==4u);
CHECK(digital_root(1681659299u)==2u);
CHECK(digital_root(1137519360u)==9u);
CHECK(digital_root(1940529389u)==5u);
CHECK(digital_root(3538678198u)==4u);
CHECK(digital_root(3395160109u)==1u);
CHECK(digital_root(924203215u)==1u);
CHECK(digital_root(3951801352u)==1u);
CHECK(digital_root(3065865433u)==7u);
CHECK(digital_root(2864782762u)==7u);
CHECK(digital_root(1356993055u)==1u);
CHECK(digital_root(703953597u)==3u);
CHECK(digital_root(361964270u)==2u);
CHECK(digital_root(1958511902u)==5u);
CHECK(digital_root(1968465316u)==4u);
CHECK(digital_root(3810760418u)==2u);
CHECK(digital_root(3773631281u)==5u);
}

CHECK(digital_root(9875)==2);CHECK(digital_root(0)==0);CHECK(digital_root(4294967295u)==3);
return 0;
}

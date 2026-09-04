#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t longest_one_run(uint32_t value);
int test_main(void) {
{
CHECK(longest_one_run(0u)==0u);
CHECK(longest_one_run(1u)==1u);
CHECK(longest_one_run(2u)==1u);
CHECK(longest_one_run(9u)==1u);
CHECK(longest_one_run(10u)==1u);
CHECK(longest_one_run(123321u)==4u);
CHECK(longest_one_run(4000000004u)==3u);
CHECK(longest_one_run(4294967295u)==32u);
CHECK(longest_one_run(264951055u)==6u);
CHECK(longest_one_run(3302568628u)==2u);
CHECK(longest_one_run(1461547428u)==3u);
CHECK(longest_one_run(4165108330u)==5u);
CHECK(longest_one_run(999144594u)==4u);
CHECK(longest_one_run(4017729701u)==4u);
CHECK(longest_one_run(969213969u)==3u);
CHECK(longest_one_run(3989968933u)==3u);
CHECK(longest_one_run(1681659299u)==4u);
CHECK(longest_one_run(1137519360u)==4u);
CHECK(longest_one_run(1940529389u)==3u);
CHECK(longest_one_run(3538678198u)==6u);
CHECK(longest_one_run(3395160109u)==4u);
CHECK(longest_one_run(924203215u)==4u);
CHECK(longest_one_run(3951801352u)==3u);
CHECK(longest_one_run(3065865433u)==4u);
CHECK(longest_one_run(2864782762u)==3u);
CHECK(longest_one_run(1356993055u)==5u);
CHECK(longest_one_run(703953597u)==5u);
CHECK(longest_one_run(361964270u)==3u);
CHECK(longest_one_run(1958511902u)==4u);
CHECK(longest_one_run(1968465316u)==3u);
CHECK(longest_one_run(3810760418u)==3u);
CHECK(longest_one_run(3773631281u)==3u);
}

CHECK(longest_one_run(110)==3);CHECK(longest_one_run(0)==0);CHECK(longest_one_run(0xffffffffu)==32);
return 0;
}

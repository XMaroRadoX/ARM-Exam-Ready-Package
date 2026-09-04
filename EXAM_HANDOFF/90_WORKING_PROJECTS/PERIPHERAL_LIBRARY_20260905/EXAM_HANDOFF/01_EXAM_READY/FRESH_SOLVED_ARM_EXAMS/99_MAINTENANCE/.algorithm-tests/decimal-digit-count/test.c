#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t decimal_digit_count(uint32_t n);
int test_main(void) {
{
CHECK(decimal_digit_count(0u)==1u);
CHECK(decimal_digit_count(1u)==1u);
CHECK(decimal_digit_count(2u)==1u);
CHECK(decimal_digit_count(9u)==1u);
CHECK(decimal_digit_count(10u)==2u);
CHECK(decimal_digit_count(123321u)==6u);
CHECK(decimal_digit_count(4000000004u)==10u);
CHECK(decimal_digit_count(4294967295u)==10u);
CHECK(decimal_digit_count(264951055u)==9u);
CHECK(decimal_digit_count(3302568628u)==10u);
CHECK(decimal_digit_count(1461547428u)==10u);
CHECK(decimal_digit_count(4165108330u)==10u);
CHECK(decimal_digit_count(999144594u)==9u);
CHECK(decimal_digit_count(4017729701u)==10u);
CHECK(decimal_digit_count(969213969u)==9u);
CHECK(decimal_digit_count(3989968933u)==10u);
CHECK(decimal_digit_count(1681659299u)==10u);
CHECK(decimal_digit_count(1137519360u)==10u);
CHECK(decimal_digit_count(1940529389u)==10u);
CHECK(decimal_digit_count(3538678198u)==10u);
CHECK(decimal_digit_count(3395160109u)==10u);
CHECK(decimal_digit_count(924203215u)==9u);
CHECK(decimal_digit_count(3951801352u)==10u);
CHECK(decimal_digit_count(3065865433u)==10u);
CHECK(decimal_digit_count(2864782762u)==10u);
CHECK(decimal_digit_count(1356993055u)==10u);
CHECK(decimal_digit_count(703953597u)==9u);
CHECK(decimal_digit_count(361964270u)==9u);
CHECK(decimal_digit_count(1958511902u)==10u);
CHECK(decimal_digit_count(1968465316u)==10u);
CHECK(decimal_digit_count(3810760418u)==10u);
CHECK(decimal_digit_count(3773631281u)==10u);
}

CHECK(decimal_digit_count(12034)==5);CHECK(decimal_digit_count(0)==1);CHECK(decimal_digit_count(123)==3);
return 0;
}

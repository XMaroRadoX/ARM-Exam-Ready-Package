#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t decimal_digit_product(uint32_t n);
int test_main(void) {
{
CHECK(decimal_digit_product(0u)==0u);
CHECK(decimal_digit_product(1u)==1u);
CHECK(decimal_digit_product(2u)==2u);
CHECK(decimal_digit_product(9u)==9u);
CHECK(decimal_digit_product(10u)==0u);
CHECK(decimal_digit_product(123321u)==36u);
CHECK(decimal_digit_product(4000000004u)==0u);
CHECK(decimal_digit_product(4294967295u)==9797760u);
CHECK(decimal_digit_product(264951055u)==0u);
CHECK(decimal_digit_product(3302568628u)==0u);
CHECK(decimal_digit_product(1461547428u)==215040u);
CHECK(decimal_digit_product(4165108330u)==0u);
CHECK(decimal_digit_product(999144594u)==2099520u);
CHECK(decimal_digit_product(4017729701u)==0u);
CHECK(decimal_digit_product(969213969u)==1417176u);
CHECK(decimal_digit_product(3989968933u)==68024448u);
CHECK(decimal_digit_product(1681659299u)==2099520u);
CHECK(decimal_digit_product(1137519360u)==0u);
CHECK(decimal_digit_product(1940529389u)==0u);
CHECK(decimal_digit_product(3538678198u)==8709120u);
CHECK(decimal_digit_product(3395160109u)==0u);
CHECK(decimal_digit_product(924203215u)==0u);
CHECK(decimal_digit_product(3951801352u)==0u);
CHECK(decimal_digit_product(3065865433u)==0u);
CHECK(decimal_digit_product(2864782762u)==3612672u);
CHECK(decimal_digit_product(1356993055u)==0u);
CHECK(decimal_digit_product(703953597u)==0u);
CHECK(decimal_digit_product(361964270u)==0u);
CHECK(decimal_digit_product(1958511902u)==0u);
CHECK(decimal_digit_product(1968465316u)==933120u);
CHECK(decimal_digit_product(3810760418u)==0u);
CHECK(decimal_digit_product(3773631281u)==127008u);
}

CHECK(decimal_digit_product(12034)==0);CHECK(decimal_digit_product(0)==0);CHECK(decimal_digit_product(123)==6);
return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t reverse_bits(uint32_t value);
int test_main(void) {
{
CHECK(reverse_bits(0u)==0u);
CHECK(reverse_bits(1u)==2147483648u);
CHECK(reverse_bits(2u)==1073741824u);
CHECK(reverse_bits(9u)==2415919104u);
CHECK(reverse_bits(10u)==1342177280u);
CHECK(reverse_bits(123321u)==2642903040u);
CHECK(reverse_bits(4000000004u)==538236535u);
CHECK(reverse_bits(4294967295u)==4294967295u);
CHECK(reverse_bits(264951055u)==4037759984u);
CHECK(reverse_bits(3302568628u)==759995171u);
CHECK(reverse_bits(1461547428u)==630110442u);
CHECK(reverse_bits(4165108330u)==1447117343u);
CHECK(reverse_bits(999144594u)==1228779996u);
CHECK(reverse_bits(4017729701u)==2769133303u);
CHECK(reverse_bits(969213969u)==2282791836u);
CHECK(reverse_bits(3989968933u)==2753055671u);
CHECK(reverse_bits(1681659299u)==3316136998u);
CHECK(reverse_bits(1137519360u)==13939650u);
CHECK(reverse_bits(1940529389u)==3070514638u);
CHECK(reverse_bits(3538678198u)==1838143307u);
CHECK(reverse_bits(3395160109u)==3020978771u);
CHECK(reverse_bits(924203215u)==4078725356u);
CHECK(reverse_bits(3951801352u)==271438295u);
CHECK(reverse_bits(3065865433u)==2603007341u);
CHECK(reverse_bits(2864782762u)==1438155605u);
CHECK(reverse_bits(1356993055u)==4165486346u);
CHECK(reverse_bits(703953597u)==3177099156u);
CHECK(reverse_bits(361964270u)==2000996776u);
CHECK(reverse_bits(1958511902u)==2023832878u);
CHECK(reverse_bits(1968465316u)==631646894u);
CHECK(reverse_bits(3810760418u)==1198113991u);
CHECK(reverse_bits(3773631281u)==2362488583u);
}

CHECK(reverse_bits(13)==0xb0000000u);CHECK(reverse_bits(0)==0);CHECK(reverse_bits(0xffffffffu)==0xffffffffu);CHECK(reverse_bits(reverse_bits(123456))==123456);
return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t word_hamming(uint32_t a, uint32_t b);
int test_main(void) {
{
CHECK(word_hamming(0u,3773631281u)==15u);
CHECK(word_hamming(1u,3810760418u)==17u);
CHECK(word_hamming(2u,1968465316u)==16u);
CHECK(word_hamming(9u,1958511902u)==16u);
CHECK(word_hamming(10u,361964270u)==13u);
CHECK(word_hamming(123321u,703953597u)==14u);
CHECK(word_hamming(4000000004u,1356993055u)==17u);
CHECK(word_hamming(4294967295u,2864782762u)==17u);
CHECK(word_hamming(264951055u,3065865433u)==20u);
CHECK(word_hamming(3302568628u,3951801352u)==16u);
CHECK(word_hamming(1461547428u,924203215u)==13u);
CHECK(word_hamming(4165108330u,3395160109u)==13u);
CHECK(word_hamming(999144594u,3538678198u)==15u);
CHECK(word_hamming(4017729701u,1940529389u)==13u);
CHECK(word_hamming(969213969u,1137519360u)==11u);
CHECK(word_hamming(3989968933u,1681659299u)==15u);
CHECK(word_hamming(1681659299u,3989968933u)==15u);
CHECK(word_hamming(1137519360u,969213969u)==11u);
CHECK(word_hamming(1940529389u,4017729701u)==13u);
CHECK(word_hamming(3538678198u,999144594u)==15u);
CHECK(word_hamming(3395160109u,4165108330u)==13u);
CHECK(word_hamming(924203215u,1461547428u)==13u);
CHECK(word_hamming(3951801352u,3302568628u)==16u);
CHECK(word_hamming(3065865433u,264951055u)==20u);
CHECK(word_hamming(2864782762u,4294967295u)==17u);
CHECK(word_hamming(1356993055u,4000000004u)==17u);
CHECK(word_hamming(703953597u,123321u)==14u);
CHECK(word_hamming(361964270u,10u)==13u);
CHECK(word_hamming(1958511902u,9u)==16u);
CHECK(word_hamming(1968465316u,2u)==16u);
CHECK(word_hamming(3810760418u,1u)==17u);
CHECK(word_hamming(3773631281u,0u)==15u);
}

CHECK(word_hamming(10,12)==2);CHECK(word_hamming(0,0xffffffffu)==32);CHECK(word_hamming(42,42)==0);
return 0;
}

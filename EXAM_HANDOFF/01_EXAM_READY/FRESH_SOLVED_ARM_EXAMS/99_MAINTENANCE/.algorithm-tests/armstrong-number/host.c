#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int armstrong_number(uint32_t n){uint32_t k=0,x=n;do{k++;x/=10;}while(x);uint64_t s=0;x=n;do{uint32_t d=x%10;uint64_t p=1;for(uint32_t i=0;i<k;i++)p*=d;s+=p;x/=10;}while(x);return s==n;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int armstrong_number(uint32_t n);
int test_main(void) {
{
CHECK(armstrong_number(0u)==1u);
CHECK(armstrong_number(1u)==1u);
CHECK(armstrong_number(2u)==1u);
CHECK(armstrong_number(9u)==1u);
CHECK(armstrong_number(10u)==0u);
CHECK(armstrong_number(123321u)==0u);
CHECK(armstrong_number(4000000004u)==0u);
CHECK(armstrong_number(4294967295u)==0u);
CHECK(armstrong_number(264951055u)==0u);
CHECK(armstrong_number(3302568628u)==0u);
CHECK(armstrong_number(1461547428u)==0u);
CHECK(armstrong_number(4165108330u)==0u);
CHECK(armstrong_number(999144594u)==0u);
CHECK(armstrong_number(4017729701u)==0u);
CHECK(armstrong_number(969213969u)==0u);
CHECK(armstrong_number(3989968933u)==0u);
CHECK(armstrong_number(1681659299u)==0u);
CHECK(armstrong_number(1137519360u)==0u);
CHECK(armstrong_number(1940529389u)==0u);
CHECK(armstrong_number(3538678198u)==0u);
CHECK(armstrong_number(3395160109u)==0u);
CHECK(armstrong_number(924203215u)==0u);
CHECK(armstrong_number(3951801352u)==0u);
CHECK(armstrong_number(3065865433u)==0u);
CHECK(armstrong_number(2864782762u)==0u);
CHECK(armstrong_number(1356993055u)==0u);
CHECK(armstrong_number(703953597u)==0u);
CHECK(armstrong_number(361964270u)==0u);
CHECK(armstrong_number(1958511902u)==0u);
CHECK(armstrong_number(1968465316u)==0u);
CHECK(armstrong_number(3810760418u)==0u);
CHECK(armstrong_number(3773631281u)==0u);
}

CHECK(armstrong_number(0));CHECK(armstrong_number(153));CHECK(armstrong_number(9474));CHECK(!armstrong_number(154));CHECK(!armstrong_number(4294967295u));
return 0;
}

int main(void){return test_main();}

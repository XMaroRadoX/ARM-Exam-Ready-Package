#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int reverse_decimal(uint32_t n,uint32_t*out){if(!out)return 0;uint64_t v=0;do{v=v*10+n%10;if(v>UINT32_MAX)return 0;n/=10;}while(n);*out=(uint32_t)v;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int reverse_decimal(uint32_t n, uint32_t *out);
int test_main(void) {
{
uint32_t property_out=77;
CHECK(reverse_decimal(0u,&property_out)&&property_out==0u);
CHECK(reverse_decimal(1u,&property_out)&&property_out==1u);
CHECK(reverse_decimal(2u,&property_out)&&property_out==2u);
CHECK(reverse_decimal(9u,&property_out)&&property_out==9u);
CHECK(reverse_decimal(10u,&property_out)&&property_out==1u);
CHECK(reverse_decimal(123321u,&property_out)&&property_out==123321u);
CHECK(reverse_decimal(4000000004u,&property_out)&&property_out==4000000004u);
CHECK(!reverse_decimal(4294967295u,&property_out));
CHECK(reverse_decimal(264951055u,&property_out)&&property_out==550159462u);
CHECK(!reverse_decimal(3302568628u,&property_out));
CHECK(!reverse_decimal(1461547428u,&property_out));
CHECK(reverse_decimal(4165108330u,&property_out)&&property_out==338015614u);
CHECK(reverse_decimal(999144594u,&property_out)&&property_out==495441999u);
CHECK(reverse_decimal(4017729701u,&property_out)&&property_out==1079277104u);
CHECK(reverse_decimal(969213969u,&property_out)&&property_out==969312969u);
CHECK(reverse_decimal(3989968933u,&property_out)&&property_out==3398699893u);
CHECK(!reverse_decimal(1681659299u,&property_out));
CHECK(reverse_decimal(1137519360u,&property_out)&&property_out==639157311u);
CHECK(!reverse_decimal(1940529389u,&property_out));
CHECK(!reverse_decimal(3538678198u,&property_out));
CHECK(!reverse_decimal(3395160109u,&property_out));
CHECK(reverse_decimal(924203215u,&property_out)&&property_out==512302429u);
CHECK(reverse_decimal(3951801352u,&property_out)&&property_out==2531081593u);
CHECK(reverse_decimal(3065865433u,&property_out)&&property_out==3345685603u);
CHECK(reverse_decimal(2864782762u,&property_out)&&property_out==2672874682u);
CHECK(!reverse_decimal(1356993055u,&property_out));
CHECK(reverse_decimal(703953597u,&property_out)&&property_out==795359307u);
CHECK(reverse_decimal(361964270u,&property_out)&&property_out==72469163u);
CHECK(reverse_decimal(1958511902u,&property_out)&&property_out==2091158591u);
CHECK(!reverse_decimal(1968465316u,&property_out));
CHECK(!reverse_decimal(3810760418u,&property_out));
CHECK(reverse_decimal(3773631281u,&property_out)&&property_out==1821363773u);
}

uint32_t v=7;CHECK(reverse_decimal(1203,&v)&&v==3021);CHECK(reverse_decimal(0,&v)&&v==0);v=99;CHECK(!reverse_decimal(4294967295u,&v)&&v==99);CHECK(reverse_decimal(123321,&v)&&v==123321);
return 0;
}

int main(void){return test_main();}

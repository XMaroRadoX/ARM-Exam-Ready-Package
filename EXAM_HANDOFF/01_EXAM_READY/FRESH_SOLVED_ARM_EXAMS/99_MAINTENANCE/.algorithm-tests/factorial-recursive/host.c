#include <stdint.h>
#include <stddef.h>
#include <limits.h>
static uint32_t fact_step(uint32_t n){return n?n*fact_step(n-1):1;}int factorial_recursive(uint32_t n,uint32_t*out){if(!out||n>12)return 0;*out=fact_step(n);return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int factorial_recursive(uint32_t n, uint32_t *out);
int test_main(void) {
{
uint32_t property_out=77;
CHECK(factorial_recursive(0,&property_out)&&property_out==1u);
CHECK(factorial_recursive(1,&property_out)&&property_out==1u);
CHECK(factorial_recursive(2,&property_out)&&property_out==2u);
CHECK(factorial_recursive(3,&property_out)&&property_out==6u);
CHECK(factorial_recursive(4,&property_out)&&property_out==24u);
CHECK(factorial_recursive(5,&property_out)&&property_out==120u);
CHECK(factorial_recursive(6,&property_out)&&property_out==720u);
CHECK(factorial_recursive(7,&property_out)&&property_out==5040u);
CHECK(factorial_recursive(8,&property_out)&&property_out==40320u);
CHECK(factorial_recursive(9,&property_out)&&property_out==362880u);
CHECK(factorial_recursive(10,&property_out)&&property_out==3628800u);
CHECK(factorial_recursive(11,&property_out)&&property_out==39916800u);
CHECK(factorial_recursive(12,&property_out)&&property_out==479001600u);
CHECK(!factorial_recursive(13,&property_out));
}

uint32_t v=0;CHECK(factorial_recursive(0,&v)&&v==1);CHECK(factorial_recursive(3,&v)&&v==6);CHECK(factorial_recursive(12,&v)&&v==479001600);CHECK(!factorial_recursive(13,&v));
return 0;
}

int main(void){return test_main();}

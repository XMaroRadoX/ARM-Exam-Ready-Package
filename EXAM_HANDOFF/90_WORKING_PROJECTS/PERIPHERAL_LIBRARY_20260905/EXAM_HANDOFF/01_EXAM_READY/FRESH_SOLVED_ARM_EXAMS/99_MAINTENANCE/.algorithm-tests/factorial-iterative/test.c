#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int factorial_iterative(uint32_t n, uint32_t *out);
int test_main(void) {
{
uint32_t property_out=77;
CHECK(factorial_iterative(0,&property_out)&&property_out==1u);
CHECK(factorial_iterative(1,&property_out)&&property_out==1u);
CHECK(factorial_iterative(2,&property_out)&&property_out==2u);
CHECK(factorial_iterative(3,&property_out)&&property_out==6u);
CHECK(factorial_iterative(4,&property_out)&&property_out==24u);
CHECK(factorial_iterative(5,&property_out)&&property_out==120u);
CHECK(factorial_iterative(6,&property_out)&&property_out==720u);
CHECK(factorial_iterative(7,&property_out)&&property_out==5040u);
CHECK(factorial_iterative(8,&property_out)&&property_out==40320u);
CHECK(factorial_iterative(9,&property_out)&&property_out==362880u);
CHECK(factorial_iterative(10,&property_out)&&property_out==3628800u);
CHECK(factorial_iterative(11,&property_out)&&property_out==39916800u);
CHECK(factorial_iterative(12,&property_out)&&property_out==479001600u);
CHECK(!factorial_iterative(13,&property_out));
}

uint32_t v=99;CHECK(factorial_iterative(0,&v)&&v==1);CHECK(factorial_iterative(4,&v)&&v==24);CHECK(factorial_iterative(12,&v)&&v==479001600);CHECK(!factorial_iterative(13,&v)&&v==479001600);
return 0;
}

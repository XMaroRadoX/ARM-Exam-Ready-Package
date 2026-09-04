#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int fibonacci_number(uint32_t n,uint32_t*out){if(!out||n>47)return 0;if(!n){*out=0;return 1;}uint32_t a=0,b=1;while(--n){uint32_t t=a+b;a=b;b=t;}*out=b;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int fibonacci_number(uint32_t n, uint32_t *out);
int test_main(void) {
{
uint32_t property_out=77;
CHECK(fibonacci_number(0,&property_out)&&property_out==0u);
CHECK(fibonacci_number(1,&property_out)&&property_out==1u);
CHECK(fibonacci_number(2,&property_out)&&property_out==1u);
CHECK(fibonacci_number(3,&property_out)&&property_out==2u);
CHECK(fibonacci_number(4,&property_out)&&property_out==3u);
CHECK(fibonacci_number(5,&property_out)&&property_out==5u);
CHECK(fibonacci_number(6,&property_out)&&property_out==8u);
CHECK(fibonacci_number(7,&property_out)&&property_out==13u);
CHECK(fibonacci_number(8,&property_out)&&property_out==21u);
CHECK(fibonacci_number(9,&property_out)&&property_out==34u);
CHECK(fibonacci_number(10,&property_out)&&property_out==55u);
CHECK(fibonacci_number(11,&property_out)&&property_out==89u);
CHECK(fibonacci_number(12,&property_out)&&property_out==144u);
CHECK(fibonacci_number(13,&property_out)&&property_out==233u);
CHECK(fibonacci_number(14,&property_out)&&property_out==377u);
CHECK(fibonacci_number(15,&property_out)&&property_out==610u);
CHECK(fibonacci_number(16,&property_out)&&property_out==987u);
CHECK(fibonacci_number(17,&property_out)&&property_out==1597u);
CHECK(fibonacci_number(18,&property_out)&&property_out==2584u);
CHECK(fibonacci_number(19,&property_out)&&property_out==4181u);
CHECK(fibonacci_number(20,&property_out)&&property_out==6765u);
CHECK(fibonacci_number(21,&property_out)&&property_out==10946u);
CHECK(fibonacci_number(22,&property_out)&&property_out==17711u);
CHECK(fibonacci_number(23,&property_out)&&property_out==28657u);
CHECK(fibonacci_number(24,&property_out)&&property_out==46368u);
CHECK(fibonacci_number(25,&property_out)&&property_out==75025u);
CHECK(fibonacci_number(26,&property_out)&&property_out==121393u);
CHECK(fibonacci_number(27,&property_out)&&property_out==196418u);
CHECK(fibonacci_number(28,&property_out)&&property_out==317811u);
CHECK(fibonacci_number(29,&property_out)&&property_out==514229u);
CHECK(fibonacci_number(30,&property_out)&&property_out==832040u);
CHECK(fibonacci_number(31,&property_out)&&property_out==1346269u);
CHECK(fibonacci_number(32,&property_out)&&property_out==2178309u);
CHECK(fibonacci_number(33,&property_out)&&property_out==3524578u);
CHECK(fibonacci_number(34,&property_out)&&property_out==5702887u);
CHECK(fibonacci_number(35,&property_out)&&property_out==9227465u);
CHECK(fibonacci_number(36,&property_out)&&property_out==14930352u);
CHECK(fibonacci_number(37,&property_out)&&property_out==24157817u);
CHECK(fibonacci_number(38,&property_out)&&property_out==39088169u);
CHECK(fibonacci_number(39,&property_out)&&property_out==63245986u);
CHECK(fibonacci_number(40,&property_out)&&property_out==102334155u);
CHECK(fibonacci_number(41,&property_out)&&property_out==165580141u);
CHECK(fibonacci_number(42,&property_out)&&property_out==267914296u);
CHECK(fibonacci_number(43,&property_out)&&property_out==433494437u);
CHECK(fibonacci_number(44,&property_out)&&property_out==701408733u);
CHECK(fibonacci_number(45,&property_out)&&property_out==1134903170u);
CHECK(fibonacci_number(46,&property_out)&&property_out==1836311903u);
CHECK(fibonacci_number(47,&property_out)&&property_out==2971215073u);
}

uint32_t v=99;CHECK(fibonacci_number(0,&v)&&v==0);CHECK(fibonacci_number(5,&v)&&v==5);CHECK(fibonacci_number(47,&v)&&v==2971215073u);CHECK(!fibonacci_number(48,&v)&&v==2971215073u);
return 0;
}

int main(void){return test_main();}

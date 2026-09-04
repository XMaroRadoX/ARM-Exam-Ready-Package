#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
uint32_t array_max_u32(const uint32_t*,uint32_t);
int test_main(void){uint32_t a[]={0,0x80000000u,7,UINT32_MAX};CHECK(array_max_u32(a,4)==UINT32_MAX);CHECK(array_max_u32(a,1)==0);return 0;}
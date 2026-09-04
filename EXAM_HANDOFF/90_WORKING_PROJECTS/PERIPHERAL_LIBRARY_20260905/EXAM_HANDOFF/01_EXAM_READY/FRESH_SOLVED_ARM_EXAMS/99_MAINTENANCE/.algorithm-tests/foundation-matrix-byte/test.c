#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
uint8_t matrix_get_u8(const uint8_t*,uint32_t,uint32_t,uint32_t);
int test_main(void){uint8_t a[]={0,1,2,128,254,255};CHECK(matrix_get_u8(a,1,3,0)==128);CHECK(matrix_get_u8(a,1,3,2)==255);CHECK(matrix_get_u8(a,0,3,1)==1);return 0;}
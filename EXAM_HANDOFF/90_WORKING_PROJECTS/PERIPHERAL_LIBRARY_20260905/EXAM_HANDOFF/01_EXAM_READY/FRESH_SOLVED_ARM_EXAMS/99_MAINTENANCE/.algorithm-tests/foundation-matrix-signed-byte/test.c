#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
int8_t matrix_get_i8(const int8_t*,uint32_t,uint32_t,uint32_t);
int test_main(void){int8_t a[]={0,1,2,-128,-2,-1};CHECK(matrix_get_i8(a,1,3,0)==-128);CHECK(matrix_get_i8(a,1,3,2)==-1);CHECK(matrix_get_i8(a,0,3,1)==1);return 0;}
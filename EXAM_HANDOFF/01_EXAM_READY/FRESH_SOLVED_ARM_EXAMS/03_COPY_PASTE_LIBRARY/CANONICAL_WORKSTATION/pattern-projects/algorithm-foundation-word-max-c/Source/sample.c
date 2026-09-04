#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
uint32_t array_max_u32(const uint32_t*,uint32_t);
int test_main(void){uint32_t a[]={0,0x80000000u,7,UINT32_MAX};CHECK(array_max_u32(a,4)==UINT32_MAX);CHECK(array_max_u32(a,1)==0);return 0;}
volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}

#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
uint32_t sum7(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t);
int test_main(void){CHECK(sum7(1,2,3,4,5,6,7)==28);CHECK(sum7(0,0,0,0,9,10,11)==30);CHECK(sum7(UINT32_MAX,1,0,0,0,0,0)==0);return 0;}
volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}

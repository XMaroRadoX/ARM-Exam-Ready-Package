#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
int32_t q15_multiply(int32_t,int32_t);
int test_main(void){int32_t x=32768;CHECK(q15_multiply(32768,16384)==16384);CHECK(q15_multiply(-32768,16384)==-16384);x=q15_multiply(x,16384);x=q15_multiply(x,16384);CHECK(x==8192);return 0;}
volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}

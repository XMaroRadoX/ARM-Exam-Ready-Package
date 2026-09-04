#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
uint32_t add_square(uint32_t,uint32_t);
int test_main(void){CHECK(add_square(3,4)==13);CHECK(add_square(0,7)==7);CHECK(add_square(65536,1)==1);return 0;}
volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}

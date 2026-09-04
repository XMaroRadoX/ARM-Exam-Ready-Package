#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
int first_equal_pair(const uint32_t*,const uint32_t*,uint32_t,uint32_t);
int test_main(void){uint32_t a[]={8,3,5},b[]={2,5,3};CHECK(first_equal_pair(a,b,3,3)==0x10002);CHECK(first_equal_pair(a,b,1,3)==-1);CHECK(first_equal_pair(a,b,0,3)==-1);CHECK(first_equal_pair(a,b,3,0)==-1);return 0;}
volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}

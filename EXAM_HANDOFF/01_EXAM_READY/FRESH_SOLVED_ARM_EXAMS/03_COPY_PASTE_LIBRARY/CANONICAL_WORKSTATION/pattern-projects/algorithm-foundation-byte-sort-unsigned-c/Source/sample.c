#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
void copyData(const uint8_t*,uint8_t*,uint32_t);
void insertionSortUnsigned(uint8_t*,uint32_t);
int test_main(void){uint8_t source[]={127,128,255,0},out[5]={0,0,0,0,77};copyData(source,out,4);insertionSortUnsigned(out,4);CHECK(out[0]==0 && out[1]==127 && out[2]==128 && out[3]==255);CHECK(out[4]==77 && source[0]==127);insertionSortUnsigned(0,0);return 0;}

volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}

#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
void algorithm_algorithm_selection_sort_unsigned_assembly(uint32_t*,uint32_t);
int test_main(void){uint32_t a[]={0xFFFFFFFFu,0,0x80000000u,7};algorithm_algorithm_selection_sort_unsigned_assembly(a,4);CHECK(a[0]==0 && a[1]==7 && a[2]==0x80000000u && a[3]==0xFFFFFFFFu);algorithm_algorithm_selection_sort_unsigned_assembly(a,0);CHECK(a[3]==0xFFFFFFFFu);return 0;}
volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}

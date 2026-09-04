#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
void pat_alg_selection_sort_001(uint32_t*,uint32_t);
int test_main(void){uint32_t a[]={0xFFFFFFFFu,0,0x80000000u,7};pat_alg_selection_sort_001(a,4);CHECK(a[0]==0 && a[1]==7 && a[2]==0x80000000u && a[3]==0xFFFFFFFFu);pat_alg_selection_sort_001(a,0);CHECK(a[3]==0xFFFFFFFFu);return 0;}
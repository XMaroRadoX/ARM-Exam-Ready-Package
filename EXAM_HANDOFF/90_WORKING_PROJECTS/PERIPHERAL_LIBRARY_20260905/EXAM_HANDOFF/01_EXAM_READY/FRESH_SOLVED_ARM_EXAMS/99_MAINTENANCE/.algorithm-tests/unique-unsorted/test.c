#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t unique_unsorted(int32_t *a, uint32_t n);
int test_main(void) {
int32_t a[]={3,1,3,2,1};CHECK(unique_unsorted(a,5)==3&&a[0]==3&&a[1]==1&&a[2]==2);CHECK(unique_unsorted(0,0)==0);
return 0;
}

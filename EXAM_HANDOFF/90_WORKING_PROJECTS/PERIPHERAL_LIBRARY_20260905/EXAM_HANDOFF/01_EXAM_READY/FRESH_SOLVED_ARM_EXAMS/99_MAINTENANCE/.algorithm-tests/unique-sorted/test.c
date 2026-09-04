#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t unique_sorted(int32_t *a, uint32_t n);
int test_main(void) {
int32_t a[]={1,1,2,3,3};CHECK(unique_sorted(a,5)==3&&a[0]==1&&a[1]==2&&a[2]==3);CHECK(unique_sorted(0,0)==0);
return 0;
}

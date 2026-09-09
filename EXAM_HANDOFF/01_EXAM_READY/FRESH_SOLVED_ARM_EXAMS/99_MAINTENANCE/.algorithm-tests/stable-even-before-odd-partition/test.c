#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int array_stable_even_first(int32_t *values, uint32_t count);
int test_main(void) {
int32_t a[]={3,2,5,4,1,77};CHECK(array_stable_even_first(a,5));
CHECK(a[0]==2&&a[1]==4&&a[2]==3&&a[3]==5&&a[4]==1&&a[5]==77);
CHECK(array_stable_even_first(0,0));CHECK(!array_stable_even_first(0,1));
return 0;
}

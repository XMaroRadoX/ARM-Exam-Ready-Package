#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int checked_array_sum(const int32_t *values, uint32_t count,
                      int64_t *sum_out);
int test_main(void) {
int32_t a[]={-4,7,9};int64_t s=99;
CHECK(checked_array_sum(a,3,&s)&&s==12);
CHECK(checked_array_sum(0,0,&s)&&s==0);
s=99;CHECK(!checked_array_sum(0,1,&s)&&s==99);
CHECK(!checked_array_sum(a,UINT32_MAX,&s)&&s==99);
return 0;
}

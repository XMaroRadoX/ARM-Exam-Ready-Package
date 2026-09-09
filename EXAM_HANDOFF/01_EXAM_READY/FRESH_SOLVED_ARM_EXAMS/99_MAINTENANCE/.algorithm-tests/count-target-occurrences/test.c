#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t count_array_target(const int32_t *values, uint32_t count, int32_t target);
int test_main(void) {
int32_t a[]={-2,0,5,-7,5};
CHECK(count_array_target(a,5,5)==2);
CHECK(count_array_target(0,4,5)==0);
CHECK(count_array_target(a,0,5)==0);
return 0;
}

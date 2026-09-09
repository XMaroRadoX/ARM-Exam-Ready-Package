#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t count_array_positive(const int32_t *values, uint32_t count);
int test_main(void) {
int32_t a[]={-2,0,5,-7,0};
CHECK(count_array_positive(a,4)==1);
CHECK(count_array_positive(0,4)==0);
CHECK(count_array_positive(a,0)==0);
return 0;
}

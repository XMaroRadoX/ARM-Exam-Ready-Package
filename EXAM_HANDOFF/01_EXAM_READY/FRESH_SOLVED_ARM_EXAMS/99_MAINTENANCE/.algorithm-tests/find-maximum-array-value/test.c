#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int array_maximum(const int32_t *values, uint32_t count, int32_t *value_out);
int test_main(void) {
int32_t a[]={7,-3,9,-3},v=77;
CHECK(array_maximum(a,4,&v)&&v==9);
v=77;CHECK(!array_maximum(a,0,&v)&&v==77);
CHECK(!array_maximum(0,1,&v)&&v==77);
return 0;
}

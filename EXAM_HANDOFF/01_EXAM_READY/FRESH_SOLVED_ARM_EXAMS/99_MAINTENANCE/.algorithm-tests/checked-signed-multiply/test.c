#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int checked_multiply_i32(int32_t left, int32_t right, int32_t *result_out);
int test_main(void) {
int32_t out=77;CHECK(checked_multiply_i32(-6,7,&out)&&out==-42);
out=77;CHECK(!checked_multiply_i32(INT32_MAX,2,&out)&&out==77);
CHECK(!checked_multiply_i32(1,2,0));
return 0;
}

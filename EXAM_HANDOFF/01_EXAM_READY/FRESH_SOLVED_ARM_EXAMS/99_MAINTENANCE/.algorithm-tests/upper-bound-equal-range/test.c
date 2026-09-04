#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
size_t upper_bound_i32(const int *a, size_t n, int key);
int test_main(void) {
int a[]={1,2,2,4};CHECK(upper_bound_i32(a,4,2)==3);CHECK(upper_bound_i32(a,4,0)==0);CHECK(upper_bound_i32(a,4,INT_MAX)==4);CHECK(upper_bound_i32(0,0,1)==0);
return 0;
}

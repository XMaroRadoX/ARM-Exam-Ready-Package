#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int32_t recursive_binary_search(const int32_t *a, uint32_t n, int32_t key);
int test_main(void) {
int32_t a[]={1,3,5,7,9},b[]={INT32_MIN,0,INT32_MAX};CHECK(recursive_binary_search(a,5,7)==3);CHECK(recursive_binary_search(a,5,8)==-1);CHECK(recursive_binary_search(b,3,INT32_MIN)==0);CHECK(recursive_binary_search(b,3,INT32_MAX)==2);CHECK(recursive_binary_search(0,0,3)==-1);
return 0;
}

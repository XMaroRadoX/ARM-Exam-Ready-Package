#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t threshold_filter(const int32_t *a, uint32_t n, int32_t threshold, int32_t *out, uint32_t capacity);
int test_main(void) {
int32_t a[]={4,-1,7,4},b[5]={0};b[4]=77;CHECK(threshold_filter(a,4,3,b,4)==3&&b[0]==4&&b[1]==7&&b[2]==4&&b[4]==77);CHECK(threshold_filter(a,4,3,b,3)==UINT32_MAX);CHECK(threshold_filter(a,4,3,a,4)==3&&a[1]==7);
return 0;
}

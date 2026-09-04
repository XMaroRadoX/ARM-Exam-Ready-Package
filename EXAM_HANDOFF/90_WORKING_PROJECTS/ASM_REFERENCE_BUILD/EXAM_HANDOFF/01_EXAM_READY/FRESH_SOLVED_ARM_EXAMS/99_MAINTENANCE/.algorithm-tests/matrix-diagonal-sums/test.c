#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int diagonal_sums(const int16_t *a, uint32_t n, int64_t *out, uint32_t capacity);
int test_main(void) {
int16_t a[]={1,2,3,4,5,6,7,8,9};int64_t o[3]={0};o[2]=77;CHECK(diagonal_sums(a,3,o,2)&&o[0]==15&&o[1]==15&&o[2]==77);CHECK(diagonal_sums(0,0,o,2)&&o[0]==0);CHECK(!diagonal_sums(a,3,o,1));
return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint64_t squared_differences_i16(const int16_t *a, const int16_t *b, uint32_t n);
int test_main(void) {
int16_t a[]={-32768,-32768},b[]={32767,32767};CHECK(squared_differences_i16(a,b,2)==8589672450ULL);CHECK(squared_differences_i16(0,0,0)==0);
return 0;
}

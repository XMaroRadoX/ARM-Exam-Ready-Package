#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
size_t u32_to_base(unsigned value, unsigned base, char *out, size_t cap);
int test_main(void) {
char o[34]={0};CHECK(u32_to_base(31,16,o,3)==2&&o[0]==49&&o[1]==70&&o[2]==0);o[0]=88;CHECK(!u32_to_base(31,16,o,2)&&o[0]==88);CHECK(u32_to_base(UINT_MAX,2,o,33)==32);
return 0;
}

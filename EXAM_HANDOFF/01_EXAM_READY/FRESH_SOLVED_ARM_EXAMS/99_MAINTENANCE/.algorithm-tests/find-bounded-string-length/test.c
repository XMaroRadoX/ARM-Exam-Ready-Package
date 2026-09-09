#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int string_length_bounded(const uint8_t *text, uint32_t capacity, uint32_t *length_out);
int test_main(void) {
uint8_t a[]="ARM",b[]={'N','O'};uint32_t n=99;
CHECK(string_length_bounded(a,4,&n)&&n==3);
n=99;CHECK(!string_length_bounded(b,2,&n)&&n==99);
CHECK(!string_length_bounded(0,4,&n)&&n==99);
return 0;
}

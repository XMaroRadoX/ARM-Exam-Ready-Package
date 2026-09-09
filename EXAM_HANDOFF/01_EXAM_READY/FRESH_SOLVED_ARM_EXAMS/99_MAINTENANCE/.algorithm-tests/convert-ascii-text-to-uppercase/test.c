#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int string_to_ascii_uppercase(uint8_t *text, uint32_t capacity);
int test_main(void) {
uint8_t a[]="Arm-m3",bad[]={'A','B'};
CHECK(string_to_ascii_uppercase(a,sizeof a));CHECK(a[0]=='A');
CHECK(a[1]=='R'&&a[4]=='M');
CHECK(!string_to_ascii_uppercase(bad,2)&&bad[0]=='A');
return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int string_concatenate_bounded(uint8_t *destination, uint32_t *length,
                               uint32_t capacity, const uint8_t *source,
                               uint32_t source_capacity);
int test_main(void) {
uint8_t a[8]="ARM",b[]="M3",bad[]={'X','Y'};uint32_t n=3;
CHECK(string_concatenate_bounded(a,&n,8,b,3)&&n==5);
CHECK(a[0]=='A'&&a[3]=='M'&&a[4]=='3'&&a[5]==0);
CHECK(!string_concatenate_bounded(a,&n,6,b,3)&&n==5);
CHECK(!string_concatenate_bounded(a,&n,8,bad,2)&&n==5);
return 0;
}

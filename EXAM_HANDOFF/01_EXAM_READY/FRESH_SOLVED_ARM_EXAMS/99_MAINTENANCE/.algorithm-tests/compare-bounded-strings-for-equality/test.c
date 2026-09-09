#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int32_t strings_equal_bounded(const uint8_t *left, uint32_t left_capacity,
                              const uint8_t *right, uint32_t right_capacity);
int test_main(void) {
uint8_t a[]="ARM",b[]="ARM",c[]="Arm",bad[]={'A','R','M'};
CHECK(strings_equal_bounded(a,4,b,4)==1);
CHECK(strings_equal_bounded(a,4,c,4)==0);
CHECK(strings_equal_bounded(a,4,bad,3)==-1);
return 0;
}

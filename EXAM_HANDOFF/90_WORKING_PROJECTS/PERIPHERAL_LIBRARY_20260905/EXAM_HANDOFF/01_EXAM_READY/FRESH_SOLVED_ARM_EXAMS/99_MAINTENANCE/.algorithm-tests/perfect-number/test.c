#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int perfect_number(uint32_t n);
int test_main(void) {
CHECK(perfect_number(6));CHECK(perfect_number(28));CHECK(!perfect_number(1));CHECK(!perfect_number(12));CHECK(!perfect_number(0));
return 0;
}

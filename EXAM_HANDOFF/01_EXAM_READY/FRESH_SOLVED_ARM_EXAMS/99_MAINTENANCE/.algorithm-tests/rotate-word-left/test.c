#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t rotate_left_u32(uint32_t value, uint32_t amount);
int test_main(void) {
CHECK(rotate_left_u32(0x12345678u,4)==0x23456781u);
CHECK(rotate_left_u32(0x12345678u,0)==0x12345678u);
CHECK(rotate_left_u32(0x12345678u,36)==0x23456781u);
return 0;
}

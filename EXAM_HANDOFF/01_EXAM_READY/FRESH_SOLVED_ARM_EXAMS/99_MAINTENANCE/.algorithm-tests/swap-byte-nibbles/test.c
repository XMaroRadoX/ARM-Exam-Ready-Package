#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint8_t swap_byte_nibbles(uint8_t value);
int test_main(void) {
CHECK(swap_byte_nibbles(0xabu)==0xbau);
CHECK(swap_byte_nibbles(0x10u)==0x01u);
CHECK(swap_byte_nibbles(0xffu)==0xffu);
return 0;
}

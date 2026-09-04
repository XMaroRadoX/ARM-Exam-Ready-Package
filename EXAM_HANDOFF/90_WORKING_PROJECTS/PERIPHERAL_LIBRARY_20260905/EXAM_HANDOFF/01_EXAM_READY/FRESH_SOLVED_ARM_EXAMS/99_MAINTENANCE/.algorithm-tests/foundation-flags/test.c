#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
uint32_t classify_and_read(int32_t);
int test_main(void){CHECK((classify_and_read(0)&0xF0000000u)==0x40000000u);CHECK((classify_and_read(-1)&0xF0000000u)==0x80000000u);CHECK((classify_and_read(1)&0xF0000000u)==0);return 0;}
#include <stdint.h>
uint32_t classify_and_read(int32_t x){return x==0?0x40000000u:x<0?0x80000000u:0;}
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

uint32_t classify_and_read(int32_t);
int test_main(void){CHECK((classify_and_read(0)&0xF0000000u)==0x40000000u);CHECK((classify_and_read(-1)&0xF0000000u)==0x80000000u);CHECK((classify_and_read(1)&0xF0000000u)==0);return 0;}
int main(void){return test_main();}

#include <stdint.h>
uint32_t classify_and_read(int32_t x){return x==0?0x40000000u:x<0?0x80000000u:0;}
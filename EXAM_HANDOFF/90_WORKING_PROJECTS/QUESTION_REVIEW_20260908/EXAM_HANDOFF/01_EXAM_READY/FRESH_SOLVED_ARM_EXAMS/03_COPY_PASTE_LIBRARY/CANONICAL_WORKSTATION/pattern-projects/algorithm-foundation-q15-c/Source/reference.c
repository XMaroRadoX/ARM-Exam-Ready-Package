#include <stdint.h>
int32_t q15_multiply(int32_t a,int32_t b){int64_t x=(int64_t)a*b;return (int32_t)(uint32_t)((uint64_t)x>>15);}
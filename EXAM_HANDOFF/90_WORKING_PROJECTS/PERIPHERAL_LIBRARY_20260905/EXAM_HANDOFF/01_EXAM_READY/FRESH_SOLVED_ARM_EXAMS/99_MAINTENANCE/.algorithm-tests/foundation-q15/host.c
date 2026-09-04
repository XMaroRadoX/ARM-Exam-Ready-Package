#include <stdint.h>
int32_t q15_multiply(int32_t a,int32_t b){int64_t x=(int64_t)a*b;return (int32_t)(uint32_t)((uint64_t)x>>15);}
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

int32_t q15_multiply(int32_t,int32_t);
int test_main(void){int32_t x=32768;CHECK(q15_multiply(32768,16384)==16384);CHECK(q15_multiply(-32768,16384)==-16384);x=q15_multiply(x,16384);x=q15_multiply(x,16384);CHECK(x==8192);return 0;}
int main(void){return test_main();}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int tribonacci_array(uint32_t*out,uint32_t n,uint32_t cap){if(n>32||n>cap||(!out&&n))return 0;for(uint32_t i=0;i<n;i++)out[i]=i<2?0:i==2?1:out[i-1]+out[i-2]+out[i-3];return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int tribonacci_array(uint32_t *out, uint32_t count, uint32_t capacity);
int test_main(void) {
uint32_t a[49]={0};a[48]=77;CHECK(tribonacci_array(a,7,7)&&a[6]==7);CHECK(!tribonacci_array(a,8,7));CHECK(tribonacci_array(0,0,0));CHECK(tribonacci_array(a,32,32)&&a[48]==77);
return 0;
}

int main(void){return test_main();}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t rle_decode(const uint8_t*p,uint32_t n,uint8_t*out,uint32_t cap){if((!p&&n)||n>UINT32_MAX/2)return UINT32_MAX;uint32_t total=0;for(uint32_t i=0;i<n;i++){uint32_t c=p[2*i];if(!c||total>UINT32_MAX-c)return UINT32_MAX;total+=c;}if(total>cap||(!out&&total))return UINT32_MAX;uint32_t k=0;for(uint32_t i=0;i<n;i++)for(uint32_t j=0;j<p[2*i];j++)out[k++]=p[2*i+1];return k;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t rle_decode(const uint8_t *pairs, uint32_t pair_count, uint8_t *out, uint32_t capacity);
int test_main(void) {
uint8_t p[]={3,65,2,66},o[6]={0};o[5]=77;CHECK(rle_decode(p,2,o,5)==5&&o[2]==65&&o[3]==66&&o[5]==77);o[0]=88;CHECK(rle_decode(p,2,o,4)==UINT32_MAX&&o[0]==88);uint8_t z[]={0,65};CHECK(rle_decode(z,1,o,5)==UINT32_MAX);CHECK(rle_decode(0,0,0,0)==0);
return 0;
}

int main(void){return test_main();}

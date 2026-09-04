#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int byte_anagram(const uint8_t*a,uint32_t n,const uint8_t*b,uint32_t m){if(n!=m||((!a||!b)&&n))return 0;uint32_t f[256]={0};for(uint32_t i=0;i<n;i++)f[a[i]]++;for(uint32_t i=0;i<n;i++){if(!f[b[i]])return 0;f[b[i]]--;}return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int byte_anagram(const uint8_t *a, uint32_t n, const uint8_t *b, uint32_t m);
int test_main(void) {
uint8_t a[]={97,97,98},b[]={97,98,97},c[]={97,98,98};CHECK(byte_anagram(a,3,b,3));CHECK(!byte_anagram(a,3,c,3));CHECK(byte_anagram(0,0,0,0));CHECK(!byte_anagram(a,3,b,2));
return 0;
}

int main(void){return test_main();}

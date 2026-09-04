#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t substring_count(const uint8_t*s,uint32_t n,const uint8_t*p,uint32_t m){if(n>INT32_MAX||(!s&&n)||(!p&&m))return UINT32_MAX;if(!m)return n+1;if(m>n)return 0;uint32_t k=0;(void)k;for(uint32_t i=0;i<=n-m;i++){uint32_t j=0;while(j<m&&s[i+j]==p[j])j++;if(j==m){k++;}}return k;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t substring_count(const uint8_t *text, uint32_t length, const uint8_t *pattern, uint32_t pattern_length);
int test_main(void) {
uint8_t s[]={97,97,97,97},p[]={97,97},z[]={98};CHECK(substring_count(s,4,p,2)==3);CHECK(substring_count(s,4,z,1)==0);CHECK(substring_count(s,4,0,0)==5);CHECK(substring_count(0,0,p,2)==0);
return 0;
}

int main(void){return test_main();}

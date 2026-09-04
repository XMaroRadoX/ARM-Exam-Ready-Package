#include <stdint.h>
#include <stddef.h>
#include <limits.h>
static int trim_space_c(uint8_t c){return c==32||(c>=9&&c<=13);}uint32_t trim_ascii(uint8_t*s,uint32_t n){if(!s)return 0;uint32_t l=0;while(l<n&&trim_space_c(s[l]))l++;while(n>l&&trim_space_c(s[n-1]))n--;uint32_t k=n-l;for(uint32_t i=0;i<k;i++)s[i]=s[l+i];return k;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t trim_ascii(uint8_t *text, uint32_t length);
int test_main(void) {
uint8_t s[]={32,9,65,66,32,10},a[]={9,32,13};CHECK(trim_ascii(s,6)==2&&s[0]==65&&s[1]==66);CHECK(trim_ascii(a,3)==0);CHECK(trim_ascii(0,0)==0);
return 0;
}

int main(void){return test_main();}

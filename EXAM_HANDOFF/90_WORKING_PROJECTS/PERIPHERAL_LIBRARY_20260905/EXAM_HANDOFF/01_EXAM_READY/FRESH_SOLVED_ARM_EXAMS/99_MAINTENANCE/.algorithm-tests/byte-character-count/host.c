#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t byte_count(const uint8_t*s,uint32_t n,uint8_t key){uint32_t c=0;if(s)for(uint32_t i=0;i<n;i++)c+=s[i]==key;return c;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t byte_count(const uint8_t *text, uint32_t length, uint8_t key);
int test_main(void) {
uint8_t a[]={0,255,0,1};CHECK(byte_count(a,4,0)==2);CHECK(byte_count(a,4,255)==1);CHECK(byte_count(0,0,0)==0);
return 0;
}

int main(void){return test_main();}

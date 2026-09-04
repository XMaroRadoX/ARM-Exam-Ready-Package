#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int prime_sieve(uint8_t*f,uint32_t n,uint32_t cap){if(!f||n>65535||cap<=n)return 0;for(uint32_t i=0;i<=n;i++)f[i]=i>=2;for(uint32_t p=2;p<=n/p;p++)if(f[p])for(uint32_t j=p*p;j<=n;j+=p)f[j]=0;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int prime_sieve(uint8_t *flags, uint32_t limit, uint32_t capacity);
int test_main(void) {
uint8_t f[12]={0};f[11]=77;CHECK(prime_sieve(f,10,11)&&f[2]&&f[3]&&f[5]&&f[7]&&!f[0]&&!f[1]&&!f[4]&&!f[9]&&f[11]==77);CHECK(!prime_sieve(f,10,10));
return 0;
}

int main(void){return test_main();}

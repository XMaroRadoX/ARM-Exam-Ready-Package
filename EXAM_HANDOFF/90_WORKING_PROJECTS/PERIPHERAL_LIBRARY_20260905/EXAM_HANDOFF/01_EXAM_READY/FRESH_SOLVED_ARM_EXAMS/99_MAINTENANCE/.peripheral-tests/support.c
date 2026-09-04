#include <stdint.h>
uint32_t SystemFrequency=100000000u;
void SystemInit(void) { SystemFrequency=100000000u; }
uint64_t __aeabi_uldivmod(uint64_t n, uint64_t d) {
  uint64_t q=0, r=0; unsigned i;
  if (!d) return 0;
  for(i=0;i<64;i++) { unsigned carry=(unsigned)(r>>63); r=(r<<1)|(n>>63); n<<=1; q<<=1; if(carry || r>=d) {r-=d; q|=1;} }
  return q;
}
#include <stddef.h>
void *memset(void*d,int c,size_t n){unsigned char*p=d;while(n--)*p++=(unsigned char)c;return d;}
void *memcpy(void*d,const void*s,size_t n){unsigned char*p=d;const unsigned char*q=s;while(n--)*p++=*q++;return d;}
void __aeabi_memset4(void*d,size_t n,int c){memset(d,c,n);}
void __aeabi_memset(void*d,size_t n,int c){memset(d,c,n);}
void __aeabi_memclr8(void*d,size_t n){memset(d,0,n);}
void __aeabi_memcpy8(void*d,const void*s,size_t n){memcpy(d,s,n);}
void __aeabi_memclr4(void*d,size_t n){memset(d,0,n);}
void __aeabi_memclr(void*d,size_t n){memset(d,0,n);}
void __aeabi_memcpy4(void*d,const void*s,size_t n){memcpy(d,s,n);}
void __aeabi_memcpy(void*d,const void*s,size_t n){memcpy(d,s,n);}

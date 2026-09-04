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

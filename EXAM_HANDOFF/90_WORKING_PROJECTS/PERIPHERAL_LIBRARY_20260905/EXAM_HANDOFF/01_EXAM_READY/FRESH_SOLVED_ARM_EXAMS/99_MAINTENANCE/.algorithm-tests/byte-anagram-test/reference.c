#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int byte_anagram(const uint8_t*a,uint32_t n,const uint8_t*b,uint32_t m){if(n!=m||((!a||!b)&&n))return 0;uint32_t f[256]={0};for(uint32_t i=0;i<n;i++)f[a[i]]++;for(uint32_t i=0;i<n;i++){if(!f[b[i]])return 0;f[b[i]]--;}return 1;}

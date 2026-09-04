#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int bytes_reverse(uint8_t*s,uint32_t n){if(!s&&n)return 0;for(uint32_t i=0;i<n/2;i++){uint8_t t=s[i];s[i]=s[n-1-i];s[n-1-i]=t;}return 1;}

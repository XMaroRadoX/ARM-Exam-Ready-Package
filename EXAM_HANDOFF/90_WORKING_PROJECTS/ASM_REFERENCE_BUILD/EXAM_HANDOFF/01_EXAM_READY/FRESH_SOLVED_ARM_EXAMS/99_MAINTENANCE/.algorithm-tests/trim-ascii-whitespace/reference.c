#include <stdint.h>
#include <stddef.h>
#include <limits.h>
static int trim_space_c(uint8_t c){return c==32||(c>=9&&c<=13);}uint32_t trim_ascii(uint8_t*s,uint32_t n){if(!s)return 0;uint32_t l=0;while(l<n&&trim_space_c(s[l]))l++;while(n>l&&trim_space_c(s[n-1]))n--;uint32_t k=n-l;for(uint32_t i=0;i<k;i++)s[i]=s[l+i];return k;}

#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
size_t u32_to_base(unsigned v,unsigned b,char*out,size_t cap){if(!out||b<2||b>16)return 0;char d[32];size_t n=0;do{unsigned x=v%b;d[n++]=(char)(x<10?48+x:55+x);v/=b;}while(v);if(cap<=n)return 0;for(size_t i=0;i<n;i++)out[i]=d[n-1-i];out[n]=0;return n;}

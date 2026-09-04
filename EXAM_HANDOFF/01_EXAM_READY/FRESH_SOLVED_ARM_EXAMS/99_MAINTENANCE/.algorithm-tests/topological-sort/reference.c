#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
size_t topological_sort(const uint8_t*a,size_t n,size_t*d,size_t*q,size_t*out){if(!a||!d||!q||!out||n>256)return 0;size_t h=0,t=0;for(size_t i=0;i<n;i++){d[i]=0;for(size_t j=0;j<n;j++)d[i]+=a[j*n+i]!=0;if(!d[i])q[t++]=i;}while(h<t){size_t v=q[h];out[h++]=v;for(size_t j=0;j<n;j++)if(a[v*n+j]&&!--d[j])q[t++]=j;}return h==n?h:0;}

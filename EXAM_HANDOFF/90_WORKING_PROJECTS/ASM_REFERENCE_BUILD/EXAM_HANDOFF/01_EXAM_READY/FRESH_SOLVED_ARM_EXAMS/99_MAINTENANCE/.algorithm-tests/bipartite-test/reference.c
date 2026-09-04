#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int graph_is_bipartite(const uint8_t*a,size_t n,int8_t*c,size_t*q){if(!a||!c||!q||n>256)return 0;for(size_t i=0;i<n;i++)c[i]=-1;for(size_t s=0;s<n;s++)if(c[s]<0){size_t h=0,t=0;c[s]=0;q[t++]=s;while(h<t){size_t v=q[h++];for(size_t w=0;w<n;w++)if(a[v*n+w]){if(c[w]<0){c[w]=1-c[v];q[t++]=w;}else if(c[w]==c[v])return 0;}}}return 1;}

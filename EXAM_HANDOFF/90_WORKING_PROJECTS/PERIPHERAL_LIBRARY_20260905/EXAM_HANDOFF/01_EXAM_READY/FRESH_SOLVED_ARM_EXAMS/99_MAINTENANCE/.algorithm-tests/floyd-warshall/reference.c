#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
int floyd_warshall(int*d,size_t n,int inf){if(!d||n>256||inf<=0)return 0;for(size_t k=0;k<n;k++)for(size_t i=0;i<n;i++)for(size_t j=0;j<n;j++)if(d[i*n+k]!=inf&&d[k*n+j]!=inf){int64_t x=(int64_t)d[i*n+k]+d[k*n+j];if(x<INT_MIN||x>INT_MAX)return 0;if(x<d[i*n+j])d[i*n+j]=(int)x;}for(size_t i=0;i<n;i++)if(d[i*n+i]<0)return 0;return 1;}

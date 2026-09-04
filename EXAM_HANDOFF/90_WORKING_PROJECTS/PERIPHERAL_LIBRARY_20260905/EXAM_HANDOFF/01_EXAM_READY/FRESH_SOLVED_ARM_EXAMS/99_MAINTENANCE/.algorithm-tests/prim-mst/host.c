#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
#include <limits.h>
unsigned prim_mst(const unsigned*w,size_t n,size_t s,unsigned*b,unsigned char*u){if(!w||!b||!u||s>=n||n>256)return UINT_MAX;for(size_t i=0;i<n;i++){b[i]=UINT_MAX;u[i]=0;}b[s]=0;unsigned total=0;for(size_t k=0;k<n;k++){size_t v=n;unsigned low=UINT_MAX;for(size_t i=0;i<n;i++)if(!u[i]&&b[i]<low){low=b[i];v=i;}if(v==n||low>=UINT_MAX-total)return UINT_MAX;u[v]=1;total+=low;for(size_t i=0;i<n;i++)if(!u[i]&&w[v*n+i]&&w[v*n+i]<b[i])b[i]=w[v*n+i];}return total;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
unsigned prim_mst(const unsigned *w, size_t n, size_t start, unsigned *best, unsigned char *used);
int test_main(void) {
unsigned w[]={0,2,9,2,0,3,9,3,0},b[3];unsigned char u[3];CHECK(prim_mst(w,3,0,b,u)==5);unsigned d[]={0,0,0,0};CHECK(prim_mst(d,2,0,b,u)==UINT_MAX);CHECK(prim_mst(d,1,0,b,u)==0);unsigned big[]={0,UINT_MAX-1,0,UINT_MAX-1,0,2,0,2,0};CHECK(prim_mst(big,3,0,b,u)==UINT_MAX);
return 0;
}

int main(void){return test_main();}

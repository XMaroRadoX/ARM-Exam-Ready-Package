#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
static int cycle_visit(const uint8_t*a,size_t n,size_t v,uint8_t*s){s[v]=1;for(size_t w=0;w<n;w++)if(a[v*n+w]){if(s[w]==1)return 1;if(!s[w]&&cycle_visit(a,n,w,s))return 1;}s[v]=2;return 0;}
int directed_cycle(const uint8_t*a,size_t n,uint8_t*s){if(!a||!s||n>256)return 0;for(size_t i=0;i<n;i++)s[i]=0;for(size_t i=0;i<n;i++)if(!s[i]&&cycle_visit(a,n,i,s))return 1;return 0;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int directed_cycle(const uint8_t *a, size_t n, uint8_t *state);
int test_main(void) {
uint8_t a[]={0,1,0,0,0,1,0,0,0},s[3];CHECK(!directed_cycle(a,3,s));a[6]=1;CHECK(directed_cycle(a,3,s));uint8_t self[]={1};CHECK(directed_cycle(self,1,s));
return 0;
}

int main(void){return test_main();}

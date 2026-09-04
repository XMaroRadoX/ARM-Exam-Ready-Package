#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int extrema_indexes(const int32_t*a,uint32_t n,uint32_t*lo,uint32_t*hi){if(!a||!n||!lo||!hi||lo==hi)return 0;uint32_t l=0,h=0;for(uint32_t i=1;i<n;i++){if(a[i]<a[l])l=i;if(a[i]>a[h])h=i;}*lo=l;*hi=h;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int extrema_indexes(const int32_t *a, uint32_t n, uint32_t *min_index, uint32_t *max_index);
int test_main(void) {
int32_t a[]={7,-2,7,-2};uint32_t l=99,h=99;CHECK(extrema_indexes(a,4,&l,&h)&&l==1&&h==0);CHECK(!extrema_indexes(a,0,&l,&h)&&l==1&&h==0);
return 0;
}

int main(void){return test_main();}

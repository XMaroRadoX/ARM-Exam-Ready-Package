#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
int quickselect(int *a,size_t n,size_t k,int *out){size_t lo=0u,hi;if(a==NULL||out==NULL||k>=n)return 0;hi=n-1u;for(;;){size_t i,j=lo;int p=a[hi];for(i=lo;i<hi;++i)if(a[i]<p){int t=a[i];a[i]=a[j];a[j++]=t;}a[hi]=a[j];a[j]=p;if(j==k){*out=a[j];return 1;}if(k<j)hi=j-1u;else lo=j+1u;}}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int quickselect(int *a, size_t n, size_t k, int *out);
int test_main(void) {
int a[]={4,1,3,2},v=0;CHECK(quickselect(a,4,1,&v)&&v==2);int b[]={2,2,2};CHECK(quickselect(b,3,2,&v)&&v==2);CHECK(!quickselect(a,4,4,&v));
return 0;
}

int main(void){return test_main();}

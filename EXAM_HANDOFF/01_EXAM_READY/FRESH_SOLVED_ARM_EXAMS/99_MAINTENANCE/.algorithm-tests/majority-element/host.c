#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int majority_element(const int32_t*a,uint32_t n,int32_t*out){if(!a||!n||!out)return 0;int32_t v=0;uint32_t votes=0,c=0;for(uint32_t i=0;i<n;i++){if(!votes){v=a[i];votes=1;}else if(v==a[i])votes++;else votes--;}for(uint32_t i=0;i<n;i++)c+=a[i]==v;if(c<=n/2)return 0;*out=v;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int majority_element(const int32_t *a, uint32_t n, int32_t *out);
int test_main(void) {
int32_t a[]={2,1,2,3,2},b[]={1,2,3,4},v=99;CHECK(majority_element(a,5,&v)&&v==2);v=99;CHECK(!majority_element(b,4,&v)&&v==99);CHECK(!majority_element(0,0,&v));
return 0;
}

int main(void){return test_main();}

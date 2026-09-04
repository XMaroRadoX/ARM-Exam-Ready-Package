#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
size_t upper_bound_i32(const int *a,size_t n,int key){size_t lo=0u,hi=n;if(a==NULL)return 0u;while(lo<hi){size_t m=lo+(hi-lo)/2u;if(a[m]<=key)lo=m+1u;else hi=m;}return lo;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
size_t upper_bound_i32(const int *a, size_t n, int key);
int test_main(void) {
int a[]={1,2,2,4};CHECK(upper_bound_i32(a,4,2)==3);CHECK(upper_bound_i32(a,4,0)==0);CHECK(upper_bound_i32(a,4,INT_MAX)==4);CHECK(upper_bound_i32(0,0,1)==0);
return 0;
}

int main(void){return test_main();}

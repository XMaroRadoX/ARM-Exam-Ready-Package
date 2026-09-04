#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int32_t recursive_binary_search(const int32_t*a,uint32_t n,int32_t key){if(!a||!n||n>INT32_MAX)return -1;uint32_t m=n/2;if(a[m]==key)return (int32_t)m;if(key<a[m])return recursive_binary_search(a,m,key);int32_t p=recursive_binary_search(a+m+1,n-m-1,key);return p<0?-1:(int32_t)(m+1)+(int32_t)p;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int32_t recursive_binary_search(const int32_t *a, uint32_t n, int32_t key);
int test_main(void) {
int32_t a[]={1,3,5,7,9},b[]={INT32_MIN,0,INT32_MAX};CHECK(recursive_binary_search(a,5,7)==3);CHECK(recursive_binary_search(a,5,8)==-1);CHECK(recursive_binary_search(b,3,INT32_MIN)==0);CHECK(recursive_binary_search(b,3,INT32_MAX)==2);CHECK(recursive_binary_search(0,0,3)==-1);
return 0;
}

int main(void){return test_main();}

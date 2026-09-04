#include <stdint.h>
int first_equal_pair(const uint32_t*a,const uint32_t*b,uint32_t n,uint32_t m){uint32_t i,j;for(i=0;i<n;i++)for(j=0;j<m;j++)if(a[i]==b[j])return (int)((i<<16)|j);return -1;}
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

int first_equal_pair(const uint32_t*,const uint32_t*,uint32_t,uint32_t);
int test_main(void){uint32_t a[]={8,3,5},b[]={2,5,3};CHECK(first_equal_pair(a,b,3,3)==0x10002);CHECK(first_equal_pair(a,b,1,3)==-1);CHECK(first_equal_pair(a,b,0,3)==-1);CHECK(first_equal_pair(a,b,3,0)==-1);return 0;}
int main(void){return test_main();}
